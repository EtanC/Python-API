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
    '''
    Searches for a channel in the data_store with the given channel_id
    Returns None if the channel was not found
    '''
    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return None

def is_channel_member(auth_user_id, members):
    '''
    Verifies if the auth_user_id is in the list of members for a channel
    '''
    for user in members:
        if user['u_id'] == auth_user_id:
            return True
    return False
            

def channel_messages_v1(auth_user_id, channel_id, start):
    '''
    Returns up to 50 messages from the specified channel given a starting index
    Also returns the starting and ending indexes of the returned messages
    Will raise InputError if
        - channel_id is invalid
        - start is greater than the total number of messages
    Will raise AccessError if
        - auth_user_id is not a member of the channel
    '''
    # Checking channel_id is valid
    channel = get_channel(channel_id)
    if channel == None:
        raise InputError("Invalid channel")
    # Checking start is valid
    if start > len(channel['messages']):
        raise InputError("Invalid start")
    # Checking auth_user_id is part of channel
    if not is_channel_member(auth_user_id, channel['all_members']):
        raise AccessError("User is not a member of the channel")
    # Returning up to 50 messages
    end = start + 50
    messages = channel['messages'][start:end]
    # Setting end to -1 if no more messages left
    if start + 50 > len(channel['messages']):
        end = -1
    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
