from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper import token_to_user, get_channel
import threading
import time
from datetime import datetime, timezone

def start_standup(user, channel_id, length):
    # Wait for messages from standup to be sent
    time.sleep(length)
    # Collect all messages from standup
    store = data_store.get()
    channel = get_channel(channel_id, store)
    standup_message = '\n'.join([
        f"{message['user']['handle_str']}: {message['message']}"
        for message in channel['standup']['messages']
    ])
    # User who initiated standup sends the message
    timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    react = [
        {
            'react_id': 1,
            'u_ids' : [], 
        },
    ]
    message = {
        'message_id' : store['message_id'],
        'u_id' : user['u_id'],
        'message' : standup_message,
        'time_created' : timestamp,
        'reacts' : [],
        'is_pinned' : False,
        'reacts' : react,
    }
    channel['messages'].insert(0, message)
    # Clean up standup since standup ended
    del channel['standup']
    data_store.set(store)
    return

def standup_start_v1(token, channel_id, length):
    store = data_store.get()
    user = token_to_user(token, store)
    if user is None:
        raise AccessError(description="Invalid token")
    channel = get_channel(channel_id, store)
    if channel is None:
        raise InputError(description="Invalid channel id")
    if not user in channel['all_members']:
        raise AccessError(description="User not a member of the channel")
    if length < 0:
        raise InputError(
            description="Invalid standup duration, must be positive integer"
        )
    # Assuming that every standup that finishes will remove key 'standup',
    # if key doesnt exist, no standup currently active
    if 'standup' in channel:
        raise InputError(description="Active standup already running in channel")
    
    standup_thread = threading.Thread(
        target=start_standup, args=(user, channel_id, length)
    )
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    channel['standup'] = {
        'initiator': user,
        'messages': [],
        'time_finish' : current_time + length
    }
    data_store.set(store)
    standup_thread.start()
    
    return {'time_finish' : current_time + length}

def standup_send_v1(token, channel_id, message): 
    store = data_store.get()
    user = token_to_user(token, store)
    if user is None:
        raise AccessError(description="Invalid token")
    channel = get_channel(channel_id, store)
    if channel is None:
        raise InputError(description="Invalid channel id")
    if not user in channel['all_members']:
        raise AccessError(description="User not a member of the channel")
    if len(message) > 1000: 
        raise InputError(description="Invalid message that exceeds 1000 characters")
    if 'standup' not in channel:
        raise InputError("Standup not active!")

    channel['standup']['messages'].append({
        'user' : user,
        'message' : message,
    })
    data_store.set(store)
    return {}
    
def standup_active_v1(token, channel_id):
    
    store = data_store.get()
    user = token_to_user(token, store)
    
    if user is None:
        raise AccessError(description="Invalid token")
    channel = get_channel(channel_id, store)
    
    if channel is None:
        raise InputError(description="Invalid channel id")
   
    if not user in channel['all_members']:
        raise AccessError(description="User not a member of the channel")

    is_active = False
    time_finish = None

    if 'standup' in channel:
        is_active = True
        time_finish = channel['standup']['time_finish']
        
    return {'is_active' : is_active , 'time_finish' : time_finish}

        
