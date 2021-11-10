from re import M
from src.data_store import data_store
from src.dm import dm_list_v1, dm_messages_v1
from src.error import InputError
from src.error import AccessError
from json import dumps
from flask import Flask, request
from src.helper import token_to_user, get_channel, decode_token, get_user, get_message, get_dm, is_global_owner
from datetime import timezone, datetime
from src.channel import channel_messages_v1, is_channel_member
from src.channels import channels_list_v1

def search_v1(token, query_str):

    if len(query_str) < 0 or len(query_str) > 1000:
        raise InputError(description= "search query is TOO SHORT or TOO LONG")

    messages = []

    all_channels = channels_list_v1(token)['channels']
    for channel in all_channels:
        channel_id = channel['channel_id']
        all_messages = channel_messages_v1(token, channel_id, 0)['messages']
        for message in all_messages:
            if query_str in message['message']:
                messages.append(message)


    all_dms  = dm_list_v1(token)['dms']
    for dm in all_dms:
        dm_id = dm['dm_id']
        all_messages = dm_messages_v1(token, dm_id, 0)['messages']
        for message in all_messages:
            if query_str in message['message']:
                messages.append(message)
    
    return {'messages': messages}