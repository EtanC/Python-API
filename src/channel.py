from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.channels import channels_list_v1, check_valid_user_id
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

#helper function that returns the user
#returns user_id (dictionary) or None
def get_user(auth_user_id, store):

    store = data_store.get()

    # if the user is valid, return the user otherise return NOTHING
    if check_valid_user_id(auth_user_id, store) == True:
        return store['users'][auth_user_id - 1]   
    
    return None

#helper function to check if the channel_id is valid
def check_valid_channel_id(channel_id, store):

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False

#helper function that return the channel
#returns channel_id (dictionary) or None
def get_channel(channel_id, store):

    store = data_store.get()
    # if the channel is valid, return the channel otherise return NOTHING
    if check_valid_channel_id(channel_id, store) == True:
        return store['channels'][channel_id - 1]   
    
    return None


def channel_join_v1(auth_user_id, channel_id):

    '''
    Given a channel_id of a channel that the authorised user can join, 
    adds them to that channel.
    auth_user_id and channel_id are in INT form
    ''' 
    
    store = data_store.get() # get the data
    channel = get_channel(channel_id, store)
    user = get_user(auth_user_id, store)

    # if channel dosent exist:
    if (channel == None):
        raise InputError("channel ID is INVALID")

    if (user == None):
        raise InputError("user is INVALID")

    else: 
        # if the user is ALREADY part of the channel:
        channel_user_list = channel['all_members']
        if user in channel_user_list: #if a dictionary exists in a list of dictionaries
            raise InputError("User ALREADY in channel")

            # if the channel is a private channel:
        if channel['is_public'] == False:
            raise AccessError("This channel is PRIVATE")
            
    # otherwise, join the user to the channel by appending
    channel['all_members'].append(user)
    data_store.set(store)

    return {
    }




