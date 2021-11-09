from re import M
from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from json import dumps
from flask import Flask, request
from src.helper import token_to_user, get_channel, decode_token, get_user, get_message, get_dm, is_global_owner
from datetime import timezone, datetime
from src.channel import is_channel_member

def message_senddm_v1(token, dm_id, message):

    token_data = decode_token(token)
    # if token is invalid or doesn't have an 'auth_user_id' which it should 
    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description="Invalid token")
        
    auth_user_id = token_data['auth_user_id']
    store = data_store.get()
    dm = get_dm(dm_id, store)
    user = token_to_user(token, store)

    # Checking if auth_user_id is valid
    if get_user(auth_user_id, store) == None:
        raise AccessError(description="auth_user_id is not valid")

    # check the token's validity:
    if user == None:
        raise AccessError(description="INVALID token passed in")

    # check message length:
    if (len(message) < 1 or len(message) > 1000):
        raise InputError(description="message is TOO SHORT or TOO LONG")

    # check dm id's validity:
    if get_dm(dm_id, store) == None:
        raise InputError(description="dm_id is INVALID")

    # check user is part of channel:
    dm_user_list = dm['members']
    if user not in dm_user_list:
        raise AccessError(description="This user is NOT part of dm")

    # using datetime to capture the time the message was created
    dt = datetime.now()
    time_created = dt.replace(tzinfo=timezone.utc).timestamp()
    
    # Get the contents for the new dm message
    dm_message_to_send = message
    user_id = user['u_id']
    message_id = store['message_id'] 
    store['message_id'] += 1
    
    # Create the new dm_message and its contents
    new_dm_message = {
        'message_id': message_id,
        'u_id': user_id,
        'message': dm_message_to_send,
        'time_created': time_created,
    }
   
    # Add the message to the dm
    all_dm_messages = dm['messages']
    all_dm_messages.append(new_dm_message)
    data_store.set(store)
    return {
        'message_id': message_id
    }

def message_remove_v1(token, message_id):
       
    # if token is invalid or doesn't have an 'auth_user_id' which it should 
    token_data = decode_token(token)
    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description='Invalid token')

    auth_user_id = token_data['auth_user_id']
    store = data_store.get()
    user = token_to_user(token, store)
    message_to_remove = get_message(message_id, store)

    # Checking if auth_user_id is valid
    if get_user(auth_user_id, store) == None:
        raise AccessError(description="auth_user_id is not valid")

    # check the token's validity:
    if user == None:
        raise AccessError(description="INVALID token passed in")

    # check message ID validity:
    if get_message(message_id, store) == None:
        raise InputError(description="message ID is INVALID")

    # check if user is allowed to edit the right message (might need to change for the owener permissions)
    # assuming no need to check if user in channel 
    if auth_user_id != message_to_remove['u_id'] and not has_owner_perms(auth_user_id, store, user, message_id): 
        raise AccessError(description="User is NOT AUTHORISED to edit message")

    # remove the message
    for i,channel in enumerate(store['channels']):
        for j,message in enumerate(channel['messages']):
            if message['message_id'] == message_id:
                del store['channels'][i]['messages'][j]

    data_store.set(store)
    return {}

def message_edit_v1(token, message_id, message):
       
    # if token is invalid or doesn't have an 'auth_user_id' which it should 
    token_data = decode_token(token)
    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description='Invalid token')
        
    auth_user_id = token_data['auth_user_id']    
    store = data_store.get()
    user = token_to_user(token, store)
    message_to_edit = get_message(message_id, store)

    # check the token's validity:
    if user == None:
        raise AccessError(description="INVALID token passed in")

    # check message length:
    if (len(message) > 1000):
        raise InputError(description="message is TOO LONG")

    # check message ID validity:
    if get_message(message_id, store) == None:
        raise InputError(description="message ID is INVALID")

    # check if user is allowed to edit the right message (might need to change for the owener permissions)
    # assuming no need to check if user in channel 
    if auth_user_id != message_to_edit['u_id'] and not has_owner_perms(auth_user_id, store, user, message_id):
        raise AccessError(description="User is NOT AUTHORISED to edit message")

    # edit the message
    message_to_edit['message'] = message

    # if the new message is empty, delete it 
    if (message_to_edit['message']) == "":
        for i,channel in enumerate(store['channels']):
            for j,message in enumerate(channel['messages']):
                if message['message_id'] == message_id:
                    del store['channels'][i]['messages'][j]

    data_store.set(store)
    return {}

def message_send_v1(token, channel_id, message):

    token_data = decode_token(token)
    # if token is invalid or doesn't have an 'auth_user_id' which it should 
    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description="Invalid token")
        
    store = data_store.get()
    channel = get_channel(channel_id, store)
    user = token_to_user(token, store)

    # check the token's validity:
    if user == None:
        raise AccessError(description="INVALID token passed in")

    # check message length:
    if (len(message) < 1 or len(message) > 1000):
        raise InputError(description="message is TOO SHORT or TOO LONG")

    # check channel id's validity:
    if get_channel(channel_id, store) == None:
        raise InputError(description="channel_id is INVALID")

    # check user is part of channel:
    channel_user_list = channel['all_members']
    if user not in channel_user_list:
        raise AccessError(description="This user is NOT part of channel")

    # obtain message_id from store and update it for later
    message_id = store['message_id'] 
    store['message_id'] += 1
    
    user_id = user['u_id']
    message_to_add = message
    
    dt = datetime.now()
    time_created = dt.replace(tzinfo=timezone.utc).timestamp()

    # create dict containing the new message info
    new_message = {}
    new_message['message_id'] = message_id
    new_message['u_id'] = user_id
    new_message['message'] = message_to_add
    new_message['time_created'] = time_created
    
    #get list of all messages (not deleted) from the channel 
    all_channel_messages = channel['messages']

    #add the new message to the channel
    all_channel_messages.append(new_message)
    data_store.set(store)
    return {
        'message_id': message_id
    }

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    Send a message from the authorised user to the DM specified by dm_id 
    automatically at a specified time in the future.
    
    Arguments: 
        token       (str)   - token identifying user
        dm_id       (int)   - ID of DM that message will be sent to 
        message     (str)   - message that will be sent
        time_sent   (int)   - unix timestamp of when the message will be sent
    
    Exceptions: 
        InputError  - invalid dm_id
                    - length of message over 1000 char 
                    - time_sent is a time of the past
        AccessError - invalid token
                    - dm_id is valid and authorised user is not a member of the dm
    
    Return Value:
        Returns { message_id } on successful call 
    '''
    
    store = data_store.get() 
    user = token_to_user(token, store)
    
    # check valid token
    if user is None: 
        raise AccessError(description='Invalid token')
    
    # check valid dm_id
    dm = get_dm(dm_id, store)
    if dm is None: 
        raise InputError(description='Invalid dm_id')

    # check if user is in dm
    if user not in dm['members']: 
        raise AccessError(description='User not in DM')
    
    # check message length
    if len(message) > 1000: 
        raise InputError(description='Message too long')
    
    # check time_sent not in past
    time_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    if (time_sent < time_now): 
        raise InputError(description='Time sent is in the past')

    # save the message_id of message that is not sent yet, move the message id
    # in store ahead by one so the message_id of message after doesn't clash 
    # with this one
    
    
    pass

def has_owner_perms(auth_user_id, store, user, message_id): 
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id: 
                if not is_channel_member(auth_user_id, channel['owner_members']) and not is_global_owner(user):
                    return False
    return True