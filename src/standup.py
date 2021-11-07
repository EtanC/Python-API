from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper import token_to_user, get_channel
from src.message import message_send_v1
import threading
import time
from datetime import datetime, timezone

def start_standup(token, channel_id, length):
    time.sleep(length)
    standup_message = ""
    store = data_store.get()
    channel = get_channel(channel_id, store)
    # If somehow standup got deleted before standup message got sent,
    # Dont send standup message
    if channel is None or 'standup' not in channel:
        return
    for message in channel['standup']['messages']:
        standup_message.append(
            f"{message['user']['handle_str']}: {message['message']}"
        )
    message_send_v1(token, channel_id, standup_message)
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
    if 'standup' in channel:
        raise InputError(description="Active standup already running in channel")
    if not user in channel['all_members']:
        raise AccessError(description="User not a member of the channel")
    standup_thread = threading.Thread(
        target=start_standup, args=(token, channel_id, store, channel, length)
    )
    channel['standup'] = {
        'initiator': user,
        'messages': [],
    }
    data_store.set(store)
    standup_thread.start()
    return {}
