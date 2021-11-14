from src.data_store import data_store
from src.error import AccessError 
from src.error import InputError 
from src.helper import decode_token, token_to_user, current_timestamp

# if it is valid it shouldnt raise an error 

'''
{channels_list_v1}

No input error -> assuming that auth_user_id is always valid. 
Provide a list of all channels (and their associated details) 
that the authorised user is part of.

'''
def channels_list_v1(token):
    store = data_store.get()
    # Checking if token refers to a valid user and is therefore valid
    user = token_to_user(token, store)
    if user is None:
        raise AccessError(description='Invalid token')
    auth_user_id = user['u_id']

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


def channels_listall_v1(token):
    store = data_store.get()
    if token_to_user(token, store) is None:
        raise AccessError(description='Invalid token')

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
{channels_create_v1}

Creates a new channel with the given name that is either a public or private channel. 
The user who created it automatically joins the channel.

Arguments: 
    token       (str)   - token of the user 
    name        (str)   - name of channel to be created
    is_public   (bool)  - whether channel is public or not 

Exceptions: 
    InputError  - name length not between 1 and 20 characters
    AccessError - unauthorised user / invalid token 

Return Value: 
    Returns { channel_id } on successful call 

'''
            
def channels_create_v1(token, name, is_public):
    store = data_store.get()
    # Search for the user from the token
    user_dict = token_to_user(token, store)
    if user_dict is None:
        raise AccessError(description='Invalid token')

    # Checking for length of channel name 
    if len(name) < 1 or len(name) > 20: 
        raise InputError(description="Channel name must be between 1 and 20 characters long")
    store = data_store.get()

    # get channel id by counting number of channels and adding one 
    channel_id = len(store['channels']) + 1 

    # Recording channels_joined data for user/stats/v1
    channels_joined = user_dict['channels_joined'][-1]['num_channels_joined']
    user_dict['channels_joined'].append({
        'num_channels_joined' : channels_joined + 1,
        'time_stamp' : current_timestamp(),
    })

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
