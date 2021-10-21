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




