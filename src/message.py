from re import M
from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from json import dumps
from flask import Flask, request
from src.helper import token_to_user, get_channel
from datetime import timezone, datetime

######
def message_send_v1(token, channel_id, message):

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

    return {
        'message_id': message_id
    }



