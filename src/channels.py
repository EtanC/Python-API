

from tests.channels_test import test_invalid_id
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
    
    # This is the dictionary we return at the end. 
    channels = {}

    # access list within channels
    list_channels = store['channels']
    member = list_channels['members']

    for u_id in list_channels: 
        if auth_user_id == member['u_id']: 
            channels.append(list_channels[u_id])
    return channels

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
    
    # This is the dictionary we return at the end. 
    channels = {}

    existing_users = store['users'] 
    list_channels = store['channels']

    for users in existing_users: 
        if auth_user_id == existing_users: 
            for channel in list_channels:
                channels.append(list_channels[('channel_id','name')])
    return channels
   
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

