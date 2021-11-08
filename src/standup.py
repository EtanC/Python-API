from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper import token_to_user, get_channel
from src.message import message_send_v1
import threading
import time
from datetime import datetime, timezone

def start_standup(user, channel_id, length):
    # Wait for messages from standup to be sent
    time.sleep(length)
    # Collect all messages from standup
    standup_message = ""
    store = data_store.get()
    channel = get_channel(channel_id, store)
    for message in channel['standup']['messages']:
        standup_message += (
            f"{message['user']['handle_str']}: {message['message']}\n"
        )
    # User who initiated standup sends the message
    timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    message = {
        'message_id' : store['message_id'],
        'u_id' : user['u_id'],
        'message' : standup_message,
        'time_sent' : timestamp,
        'reacts' : [],
        'is_pinned' : False,
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
    if length < 0:
        raise InputError(
            description="Invalid standup duration, must be positive integer"
        )
    # Assuming that every standup that finishes will remove key 'standup',
    # if key doesnt exist, no standup currently active
    if 'standup' in channel:
        raise InputError(description="Active standup already running in channel")
    if not user in channel['all_members']:
        raise AccessError(description="User not a member of the channel")
    standup_thread = threading.Thread(
        target=start_standup, args=(user, channel_id, length)
    )
    channel['standup'] = {
        'initiator': user,
        'messages': [],
    }
    data_store.set(store)
    standup_thread.start()
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    return {'time_finish' : current_time + length}
