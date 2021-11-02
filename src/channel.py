from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.channels import channels_list_v1, check_valid_user_id
import re
from src.helper import decode_token, token_to_user, get_channel, get_user, is_global_owner

def channel_invite_v1(token, channel_id, u_id):
    '''
    Given a channel_id of a channel that the authorised user is a member of, 
    this authorised user can invite a new user to the channel.

    Arguments:
        token (str): token identifying user 
        channel_id (int): id of channel 
        u_id (int): id of user

    Exceptions: 
        InputError  - Invalid channel id
                    - Invalid u_id
                    - u_id already in channel
        AccessError - token is not a member of the channel

     Returns: 
        Returns {} on successful creation 
    '''

    store = data_store.get()
    
    token_data = decode_token(token)

    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description='Invalid token')

    auth_user_id = token_data['auth_user_id']
    channel = get_channel(channel_id, store)
    user = get_user(auth_user_id, store)

    # if channel dosen't exist:
    if (channel == None):
        raise InputError(description="Invalid channel id")

    if (user == None):
        raise AccessError(description='Invalid token, auth_user_id does not refer to a valid user')

    if check_member_in_channel(auth_user_id, channel_id, store) == False:
        raise AccessError(description="Authorised user not a member of channel")

    # check whether member is in the channel or not 
    if check_member_in_channel(u_id, channel_id, store) == True: 
        raise InputError(description="Authorised user is already a member of the channel")

    # check for invalid u_id
    if check_valid_user_id(u_id, store) == False: 
        raise InputError(description="Invalid u_id")
  
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

def channel_details_v1(token, channel_id):
    '''
    Given a channel with ID channel_id that the authorised user is a member of, 
    provide basic details about the channel.

    Arguments: 
        token       (str) - token of user 
        channel_id  (int) - id of channel to return details of 
    
    Exceptions: 
        InputError  - channel_id invalid 
        AccessError - authorised user not a member of channel 
                    - user not authorised / invalid token 
    
    Return Value: 
        Returns { name , is_public , owner_members , all_members } on successful call
    '''
    token_data = decode_token(token)
    
    # if token is invalid or doesn't have an 'auth_user_id' which it should 
    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description='Invalid token')

    auth_user_id = token_data['auth_user_id']

    store = data_store.get() 

    # check for invalid user id 
    if check_valid_user_id(auth_user_id, store) == False: 
        raise AccessError(description="Invalid auth_user_id")
    
    # check for invalid channel id 
    if check_valid_channel(channel_id, store) == False: 
        raise InputError(description="Invalid channel id")

    # check whether member is in the channel or not 
    if check_member_in_channel(auth_user_id, channel_id, store) == False: 
        raise AccessError(description="Authorised user is not a member of the channel")

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
        raise AccessError(description="User is not a member of the channel")
    # Checking start is valid
    if start > len(channel['messages']):
        raise InputError(description="Invalid start")
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

#helper function to check if the channel_id is valid
def check_valid_channel(channel_id, store): 
    result = False 

    # if channel_id exists return True, else return False 
    for channel in store['channels']: 
        if channel_id == channel['channel_id']: 
            result = True
    return result

def channel_join_v1(token, channel_id):

    token_data = decode_token(token)

    # if token is invalid or doesn't have an 'auth_user_id' which it should 
    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description='Invalid token')

    auth_user_id = token_data['auth_user_id']


    store = data_store.get() # get the data
    channel = get_channel(channel_id, store)
    user = get_user(auth_user_id, store)

    # if channel dosen't exist:
    if (channel == None):
        raise InputError(description="channel ID is INVALID")

    if (user == None):
        raise AccessError(description="user is INVALID")

    else: 
        # if the user is ALREADY part of the channel:
        # includes the channel creator
        channel_user_list = channel['all_members']
        if user in channel_user_list: 
            raise InputError(description="User ALREADY in channel")

        # if the channel is a private channel:
        if channel['is_public'] == False:
            # If the user is not a global user
            if not is_global_owner(user):
                raise AccessError(description="This channel is PRIVATE")
            
    # otherwise, join the user to the channel by appending
    channel['all_members'].append(user)
    data_store.set(store)

    return {
    }

def channel_leave_v1(token, channel_id):
    '''
    Will remove the member from the specified channel

    Arguments:
        token       (str)      - The user's token, used to identify and
                                 validate users
        channel_id  (int)      - The channel's id, used to identify channel

    Exceptions:
        InputError  - channel_id does not refer to a valid channel
        AccessError - channel_id is valid and authorised user is not a member
                      of the channel
                    - user_id does not refer to a valid user

    Return Value:
        Returns {} on successful call
    '''
    store = data_store.get()
    # Checking if token is valid
    user = token_to_user(token, store)
    if user == None:
        raise AccessError("Invalid token")
    # Checking channel_id is valid
    channel = get_channel(channel_id, store)
    if channel == None:
        raise InputError("Invalid channel")
    # Checking if user is a member of the channel
    if not is_channel_member(user['u_id'], channel['all_members']):
        raise AccessError("User is not a channel member")
    # Remove user from channel
    channel['all_members'].remove(user)
    if is_channel_member(user['u_id'], channel['owner_members']):
        channel['owner_members'].remove(user)
    data_store.set(store)
    return {}

def channel_addowner_v1(token, channel_id, u_id):
    '''
    Will add an owner to a channel
    '''
    store = data_store.get()
    # Checking if token is valid
    current_owner = token_to_user(token, store)
    if current_owner == None:
        raise AccessError(description="Invalid token")
    # Checking channel_id is valid
    channel = get_channel(channel_id, store)
    if channel == None:
        raise InputError(description="Invalid channel")
    # Checking if inviting user has owner permissions
    if not is_channel_member(current_owner['u_id'], channel['owner_members']):
        raise AccessError(description="User does not have owner permissions")
    # Checking if u_id is valid
    user = get_user(u_id, store)
    if user == None:
        raise InputError("Invalid u_id")
    # Checking if user is member of channel
    if not is_channel_member(user['u_id'], channel['all_members']):
        raise InputError(
            description = "Can't add owner; user is not member of channel"
        )
    # Checking if user is an owner already
    if is_channel_member(user['u_id'], channel['owner_members']):
        raise InputError(
            description = "Can't add owner; user is already an owner"
        )
    channel['owner_members'].append(user)
    data_store.set(store)
    return {}

def channel_removeowner_v1(token, channel_id, u_id):
    '''
    Will remove an owner from a channel
    '''
    store = data_store.get()
    # Checking if token is valid
    current_owner = token_to_user(token, store)
    if current_owner == None:
        raise AccessError(description="Invalid token")
    # Checking channel_id is valid
    channel = get_channel(channel_id, store)
    if channel == None:
        raise InputError(description="Invalid channel")
    # Checking if inviting user has owner permissions
    if not is_channel_member(current_owner['u_id'], channel['owner_members']):
        if not is_global_owner(current_owner):
            raise AccessError(description="User does not have owner permissions")
    # Checking if u_id is valid
    user = get_user(u_id, store)
    if user == None:
        raise InputError(description="Invalid u_id")
    # Checking if user is an owner
    if is_channel_member(user['u_id'], channel['owner_members']) == False:
        raise InputError(
            description = "Can't remove owner; user is not an owner in channel"
        )
    # Checking if user is the only owner in the channel
    if len(channel['owner_members']) == 1:
        raise InputError(
            description = "Can't remove the only owner of the channel"
        )
    channel['owner_members'].remove(user)
    data_store.set(store)
    return {}

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
