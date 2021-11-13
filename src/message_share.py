from re import M
from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from json import dumps
from flask import Flask, request
from src.helper import token_to_user, get_channel, decode_token, get_user, get_message, get_dm, is_global_owner
from datetime import timezone, datetime
from src.channel import is_channel_member

def message_send_v1(token, og_message_id, message, channel_id, dm_id):

    store = data_store.get()

    user = token_to_user(token, store)
    if user is None:
        raise AccessError(description='Invalid token')

    channel = get_channel(channel_id, store)
    dm = get_dm(dm_id, store)

    # check message length:
    if (len(message) < 1 or len(message) > 1000):
        raise InputError(description="message is TOO SHORT or TOO LONG")

    # check channel id's validity:
    if get_channel(channel_id, store) is None and get_dm(dm_id, store) is None:
        raise InputError(description="channel_id and dm_id is INVALID")

    if channel_id == -1 and dm_id == -1:
        raise InputError(description="one of channel_id or dm_id must be -1")

    if og_message_id not in channel['messages']['message_id']:
        raise InputError(description="Invalid message for channel")
        
    # check user is part of channel:
    channel_user_list = channel['all_members']
    if user not in channel_user_list:
        raise AccessError(description="This user is NOT part of channel")

    # obtain message_id from store and update it for later
    message_id = store['message_id'] 
    store['message_id'] += 1
    
    user_id = user['u_id']
    message_to_add = message

    # Section for notifications
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

    if channel_id == -1:
        for messages in dm['messages']:
            if og_message_id == messages['message_id']:
                og_message = messages['message']
    elif dm_id == -1:
        for messages in channel['messages']:
            if og_message_id == messages['message_id']:
                og_message = messages['message']

    # create dict containing the new message info
    new_message = {}
    new_message['message_id'] = message_id
    new_message['u_id'] = user_id
    new_message['message'] = og_message + message_to_add
    new_message['time_created'] = time_created
    new_message['reacts'] = react

    #add the new message to the channel
    if channel_id == -1:
        all_dm_messages = dm['messages']
        all_dm_messages.insert(0, new_message)
    elif dm_id == -1:
        all_channel_messages = channel['messages']
        all_channel_messages.insert(0, new_message)

    data_store.set(store)
    return {
        'shared_message_id': message_id
    }
