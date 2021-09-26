from src.data_store import data_store
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def get_channel(channel_id):
    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return None

def is_channel_member(auth_user_id, members):
    for user in members:
        if user['u_id'] == auth_user_id:
            return True
    return False
            

def channel_messages_v1(auth_user_id, channel_id, start):
    # Checking channel_id is valid
    channel = get_channel(channel_id)
    if channel == None:
        raise InputError("Invalid channel")
    # Checking start is valid
    if start > len(channel['messages']):
        raise InputError("Invalid start")
    # Checking auth_user_id is part of channel
    if is_channel_member(auth_user_id, channel['members']):
        raise AccessError("User is not a member of the channnel")

    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
