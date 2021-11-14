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

    # Section for notifications when tagging someone in a dm
    handle = ''

    for words in dm_message_to_send.split():
        if '@' in words:
            handle = words[1:]

    shortened_message = dm_message_to_send[0:20]

    for dms in store['dms']:
        if dm_id == dms['dm_id']:
            dm_name = dms['name']
            dm_members = dms['members']

    for users in dm_members:
        if handle == users['handle_str']:
            users['notifications'].insert(0, 
                {
                "channel_id": -1,
                "dm_id": dm_id,
                "notification_message": f'{user["handle_str"]} tagged you in {dm_name}: {shortened_message}'
                }
            )

     # react dictionary
    react = [
        {
            'react_id': 1,
            'u_ids' : [], 
        },
    ]
    
    # Create the new dm_message and its contents
    new_dm_message = {
        'message_id': message_id,
        'u_id': user_id,
        'message': dm_message_to_send,
        'time_created': time_created,
        'reacts' : react
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

    # Section to insert into notifications when a message is edited
    handle = ''

    for words in message.split():
        if '@' in words:
            handle = words[1:]

    shortened_message = message[0:20]

    # Retrieving channel_id
    for channels in store['channels']:
        for messages in channels['messages']:
            if message_id == messages['message_id']:
                channel_id = channels['channel_id']

    for channels in store['channels']:
        if channel_id == channels['channel_id']:
            channel_name = channels['name']
            channel_members = channels['all_members']

    for users in channel_members:
        if handle == users['handle_str']:
            users['notifications'].insert(0, 
                {
                "channel_id": channel_id,
                "dm_id": -1,
                "notification_message": f'{user["handle_str"]} tagged you in {channel_name}: {shortened_message}'
                }
            )

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

    # Section for notifications when tagging someone in a channel
    handle = ''

    for words in message_to_add.split():
        if '@' in words:
            handle = words[1:]

    shortened_message = message_to_add[0:20]

    for channels in store['channels']:
        if channel_id == channels['channel_id']:
            channel_name = channels['name']
            channel_members = channels['all_members']

    for users in channel_members:
        if handle == users['handle_str']:
            users['notifications'].insert(0, 
                {
                "channel_id": channel_id,
                "dm_id": -1,
                "notification_message": f'{user["handle_str"]} tagged you in {channel_name}: {shortened_message}'
                }
            )

    
    dt = datetime.now()
    time_created = dt.replace(tzinfo=timezone.utc).timestamp()

    # react dictionary
    react = [
        {
            'react_id': 1,
            'u_ids' : [], 
        },
    ]

    # create dict containing the new message info
    new_message = {}
    new_message['message_id'] = message_id
    new_message['u_id'] = user_id
    new_message['message'] = message_to_add
    new_message['time_created'] = time_created
    new_message['reacts'] = react
    
    #get list of all messages (not deleted) from the channel 
    all_channel_messages = channel['messages']

    #add the new message to the channel
    all_channel_messages.insert(0, new_message)
    data_store.set(store)
    return {
        'message_id': message_id
    }

def has_owner_perms(auth_user_id, store, user, message_id): 
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id: 
                if not is_channel_member(auth_user_id, channel['owner_members']) and not is_global_owner(user):
                    return False
    return True