from src.data_store import data_store
from src.error import AccessError 
from src.error import InputError 

# if it is valid it shouldnt raise an error 


'''
{channels_list_v1}

No input error -> assuming that auth_user_id is always valid. 
Provide a list of all channels (and their associated details) 
that the authorised user is part of.

'''
def channels_list_v1(auth_user_id):
    store = data_store.get()

    # merged from master, usual check of auth_user_id
    if check_valid_user_id(auth_user_id, store) == False: 
        raise AccessError("Invalid auth_user_id")

    # access list within channels
    list_channels = store['channels']

    # a list of dictionary that we return
    auth_user_channels = []
    return_dict = {'channels' : auth_user_channels}

    for channel in list_channels:
        # if auth_user_id matches a user_id in the channel, records the channel name and id.
        for users in channel['all_members']:
            if users['u_id'] == auth_user_id: 
                new_dict = {'channel_id' :  channel['channel_id'], 'name' : channel['name']}
                auth_user_channels.append(new_dict)

    return return_dict

'''
===========================================================================
{channels_listall_v1}

Provide a list of all channels, including private channels, (and their associated details)

'''
def channels_listall_v1(auth_user_id):
    store = data_store.get()

    # merged from master, usual check of auth_user_id
    if check_valid_user_id(auth_user_id, store) == False: 
        raise AccessError("Invalid auth_user_id")

    list_channels = store['channels']
    # a list of dictionary that we return
    all_channels = []
    return_dict = {'channels' : all_channels}

    for channels in list_channels:
        new_dict = {'channel_id' :  channels['channel_id'], 'name' : channels['name']}
        all_channels.append(new_dict)
    return return_dict
   
'''
===============================================================================
'''
            
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

