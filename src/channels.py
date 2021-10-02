from src.data_store import data_store
from src.error import InputError 
from src.error import AccessError 

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    # Checking for length of channel name 
    if len(name) < 1 or len(name) > 20: 
        raise InputError("Channel name must be between 1 and 20 characters long")


    store = data_store.get()

    if check_valid_user_id(auth_user_id, store) == False: 
        raise AccessError("Invalid auth_user_id")

    # get channel id by counting number of channels and adding one 
    channel_id = len(store['channels']) + 1 

    # based on auth_user_id passed in, copy creator user's dictionary into user_dict
    user_dict = {} 
    for users in store['users']: 
        if auth_user_id == users['u_id']: 
            user_dict = users 

    # Store channel data in a dictionary 
    channel_data = { 
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [user_dict],
        'all_members': [user_dict], 
        'messages': [],
    }
    
    # Append channel_data to 'channels' list in data_store 
    store['channels'].append(channel_data)
    data_store.set(store)
    
    return {
        'channel_id': channel_id,
    }

# check if user id is valid 
def check_valid_user_id(auth_user_id, store): 
    result = False 

    # if auth_user_id exists, return true, else return false 
    for users in store['users']: 
        if auth_user_id == users['u_id']: 
            result = True

    return result
