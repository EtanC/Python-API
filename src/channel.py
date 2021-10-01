from src.data_store import data_store
from src.error import InputError, AccessError
from src.channels import check_valid_user_id


def channel_invite_v1(auth_user_id, channel_id, u_id):

    store = data_store.get()

    # check for invalid user id 
    if check_valid_user_id(auth_user_id, store) == False: 
        raise AccessError("Invalid auth_user_id")

    # check for invalid u_id
    if check_valid_user_id(u_id, store) == False: 
        raise InputError("Invalid u_id")
    
    # check for invalid channel id 
    if check_valid_channel(channel_id, store) == False: 
        raise InputError("Invalid channel id")

    # check whether member is in the channel or not 
    if check_member_in_channel(auth_user_id, channel_id, store) == True: 
        raise InputError("Authorised user is already a member of the channel")

    new_member = {}

    users_list = store['users']
    for users in users_list:
        if users['u_id'] == u_id:
            new_member = users

    channels_list = store['channels']
    for channels in channels_list:
        if  channels['channel_id'] == channel_id:
            channels['all_members'].append(new_member)

    data_store.set()

    return {}


def valid_user_id(u_id):
    store = data_store.get()

    for user in store['users']:
        if user['user_id'] == u_id:
            return True
    return False

def valid_channel_id(channel_id):
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False

def not_in_channel(channel_id, u_id):
    pass
def not_authorised_user(auth_user_id):
    pass

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

def channel_messages_v1(auth_user_id, channel_id, start):
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

def check_valid_channel(channel_id, store): 
    result = False 

    # if channel_id exists return True, else return False 
    for channel in store['channels']: 
        if channel_id == channel['channel_id']: 
            result = True
    return result 

def check_member_in_channel(auth_user_id, channel_id, store): 
    # put user info dictionaru into user_data 
    user_data = {} 
    for user in store['users']: 
        if auth_user_id == user['u_id']: 
            user_data = user
            break

    # put channel data into channel_data
    channel_data = {}
    for channel in store['channels']: 
        if channel_id == channel['channel_id']: 
            channel_data = channel 
            break
    
    # if user in members section of channel, return True else return False
    if user_data in channel_data['all_members']: 
        return True
    else: 
        return False 

def find_channel(channel_id, store): 

    for channel in store['channels']: 
        if channel_id == channel['channel_id']: 
            return channel 
