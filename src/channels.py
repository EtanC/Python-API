from src.data_store import data_store
from src.error import InputError 

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
    if (len(name) < 1) or (len(name) > 20): 
        raise InputError("Channel name must be between 1 and 20 characters long")


    store = data_store.get()

    channel_id = len(store['channels']) + 1 

    # Store channel data in a dictionary 
    channel_data = { 
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id], 

    }
    
    # Append channel_data to 'channels' list in data_store 
    store['channels'].append(channel_data)


    return {
        'channel_id': channel_id,
    }
