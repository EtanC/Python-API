from data_store import data_store
from error import AccessError 
from error import InputError 

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
    member = list_channels['all_members']

    # This is the dictionary we return at the end. 
    channel_id = []
    channel_name = []

    # if auth_user_id matches a user_id in the channel, records the channel name and id. 
    for channels in list_channels: 
        for users in member: 
            if auth_user_id == member['users']:
                channel_id.append(list_channels['channel_id'])
                channel_name.append(list_channels['name'])

    # merge the channel_id with channel_name into one dictionary
    channel = dict(zip(channel_id, channel_name))

    return channel

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
    channel_id = []
    channel_name = []

    list_channels = store['channels']
    id = list_channels['channel_id']
    name = list_channels['name']

    for channels in list_channels: 
        channel_id.append(id)
        channel_name.append(name)
    # merge the list of channel_id and name into one dictionary
    channel = dict(zip(channel_id, channel_name))

    return channel
   
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

