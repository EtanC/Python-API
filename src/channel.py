from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.channels import channels_list_v1, check_valid_user_id
from copy import deepcopy
from src.helper import decode_token, token_to_user, get_channel, get_user
import re

def channel_invite_v1(auth_user_id, channel_id, u_id):

    store = data_store.get()

    # check for invalid user id 
    if check_valid_user_id(auth_user_id, store) == False: 
        raise AccessError("Invalid auth_user_id")

    # check for invalid channel id 
    if check_valid_channel(channel_id, store) == False: 
        raise InputError("Invalid channel id")

    if check_member_in_channel(auth_user_id, channel_id, store) == False:
        raise AccessError("Authorised user not a member of channel")

    # check for invalid u_id
    if check_valid_user_id(u_id, store) == False: 
        raise InputError("Invalid u_id")

    # check whether member is in the channel or not 
    if check_member_in_channel(u_id, channel_id, store) == True: 
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

    data_store.set(store)

    return {}

def channel_details_v1(auth_user_id, channel_id):

    store = data_store.get() 

    # check for invalid user id 
    if check_valid_user_id(auth_user_id, store) == False: 
        raise AccessError("Invalid auth_user_id")
    
    # check for invalid channel id 
    if check_valid_channel(channel_id, store) == False: 
        raise InputError("Invalid channel id")

    # check whether member is in the channel or not 
    if check_member_in_channel(auth_user_id, channel_id, store) == False: 
        raise AccessError("Authorised user is not a member of the channel")

    # copying member and owner list into temporary lists 
    channel = find_channel(channel_id, store) 

    # go through the members and owners and copy everything required 
    # into a new list to return 
    mem_list = [] 
    own_list = [] 
    
    for member in channel['all_members']: 
        mem_list.append({
            'u_id': member['u_id'], 
            'email': member['email'], 
            'name_first': member['name_first'], 
            'name_last': member['name_last'], 
            'handle_str': member['handle_str'], 
        })
    
    for owner in channel['owner_members']: 
        own_list.append({
            'u_id': owner['u_id'], 
            'email': owner['email'], 
            'name_first': owner['name_first'], 
            'name_last': owner['name_last'], 
            'handle_str': owner['handle_str'], 
        })
   
    return {
        'name': channel['name'],
        'is_public': channel['is_public'], 
        'owner_members': own_list,
        'all_members': mem_list,
    }

def is_channel_member(auth_user_id, members):
    '''
    Verifies if the auth_user_id is in the list of members for a channel
    '''
    for user in members:
        if user['u_id'] == auth_user_id:
            return True
    return False
            
def channel_messages_v1(token, channel_id, start):
    '''
    Returns up to 50 messages from the specified channel given a starting index
    Also returns the starting and ending indexes of the returned messages
    Will raise InputError if
        - channel_id is invalid
        - start is greater than the total number of messages
    Will raise AccessError if
        - auth_user_id is not valid
        - auth_user_id is not a member of the channel
    '''
    store = data_store.get()
    # Checking if auth_user_id is valid
    user = token_to_user(token, store)
    if user == None:
        raise AccessError("token is not valid")
    # Checking channel_id is valid
    channel = get_channel(channel_id, store)
    if channel == None:
        raise InputError("Invalid channel")
    # Checking auth_user_id is part of channel
    if not is_channel_member(user['u_id'], channel['all_members']):
        raise AccessError("User is not a member of the channel")
    # Checking start is valid
    if start > len(channel['messages']):
        raise InputError("Invalid start")
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


#helper function that returns the user
#returns user_id (dictionary) or None
def get_user(auth_user_id, store):

    store = data_store.get()

    # if the user is valid, return the user otherwise return NOTHING
    if check_valid_user_id(auth_user_id, store) == True:
        return store['users'][auth_user_id - 1]   
    
    return None

#helper function to check if the channel_id is valid
def check_valid_channel(channel_id, store): 
    result = False 

    # if channel_id exists return True, else return False 
    for channel in store['channels']: 
        if channel_id == channel['channel_id']: 
            result = True
    return result     

#helper function that return the channel
#returns channel_id (dictionary) or None
def get_channel(channel_id, store):

    store = data_store.get()
    # if the channel is valid, return the channel otherwise return NOTHING
    if check_valid_channel(channel_id, store) == True:
        return store['channels'][channel_id - 1]   
    
    return None


def channel_join_v1(auth_user_id, channel_id):
    
    store = data_store.get() # get the data
    channel = get_channel(channel_id, store)
    user = get_user(auth_user_id, store)

    # if channel dosen't exist:
    if (channel == None):
        raise InputError("channel ID is INVALID")

    if (user == None):
        raise AccessError("user is INVALID")

    else: 
        # if the user is ALREADY part of the channel:
        # includes the channel creator
        channel_user_list = channel['all_members']
        if user in channel_user_list: 
            raise InputError("User ALREADY in channel")

        # if the channel is a private channel:
        if channel['is_public'] == False:
            raise AccessError("This channel is PRIVATE")
            
    # otherwise, join the user to the channel by appending
    channel['all_members'].append(user)
    data_store.set(store)

    return {
    }

def check_member_in_channel(auth_user_id, channel_id, store): 
    # put user info dictionary into user_data 
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
    return None 
