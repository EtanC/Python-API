from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper import token_to_user, get_channel
import threading

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
    return {}
