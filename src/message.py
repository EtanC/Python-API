from re import M
from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from json import dumps
from flask import Flask, request
from src.helper import token_to_user, get_channel, decode_token, get_user, get_message
from datetime import timezone, datetime

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
    if auth_user_id != message_to_edit['u_id']:
        raise AccessError(description="User is NOT AUTHORISED to edit message")

    # edit the message
    message_to_edit['message'] = message

    # if the new message is empty, delete it 
    if (message_to_edit['message']) == "":
        for i,channel in enumerate(store['channels']):
            for j,message in enumerate(channel['messages']):
                if message['message_id'] == message_id:
                    del store['channels'][i]['messages'][j]

    return {}


def message_send_v1(token, channel_id, message):

    token_data = decode_token(token)
    # if token is invalid or doesn't have an 'auth_user_id' which it should 
    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description="Invalid token")
        
    store = data_store.get()
    channel = get_channel(channel_id, store)
    user = token_to_user(token, store)

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

    return {
        'message_id': message_id
    }


def message_edit_v1(token, message_id, message):
       
    # if token is invalid or doesn't have an 'auth_user_id' which it should 
    token_data = decode_token(token)
    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description='Invalid token')
    auth_user_id = token_data['auth_user_id']

    store = data_store.get()
    user = token_to_user(token, store)
    message_to_edit = get_message(message_id, store)

    # Checking if auth_user_id is valid
    if get_user(auth_user_id, store) == None:
        raise AccessError(description="auth_user_id is not valid")

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
    if auth_user_id != message_to_edit['u_id']:
        raise AccessError(description="User is NOT AUTHORISED to edit message")

    # edit the message
    message_to_edit['message'] = message

    # if the new message is empty, delete it 
    if (message_to_edit['message']) == "":
        for i,channel in enumerate(store['channels']):
            for j,message in enumerate(channel['messages']):
                if message['message_id'] == message_id:
                    del store['channels'][i]['messages'][j]

    return {}




