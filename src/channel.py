from src.data_store import data_store
from src.error import InputError
from src.error import AccessError

import re

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    '''
    YOU SHOULD BE ABLE TO READ ALL THIS INSIDE "channel_join_v1_BenH" branch
    '''

    #Given a channel_id of a channel that the authorised user can join, 
    #adds them to that channel.
    #auth_user_id and channel_id are in integer form


    #channel_id does not refer to a valid channel
    if ...:
        raise InputError("channel_id is INVALID")

    #the authorised user is already a member of the channel
    if ...:
        raise InputError("User already in channel")

    #channel_id refers to a channel that is private 
    #and the authorised user is not already a channel member 
    #and is not a global owner

    store = data_store.get()
    for channel in store['channels']:
        if channel['Private'] == True:
            raise AccessError("This channel is PRIVATE")


        
    return {
    }
