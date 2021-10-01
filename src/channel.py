from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.channels import channels_list_v1

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

            {



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


#helper function to find if a channel exists based on the id
def valid_channel_id(channel_id):

    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False

#helper function to find if a channel exists based on the id
def find_user_in_channel(auth_user_id, channel_id):

    store = data_store.get()
    channels_list = channels_list_v1(auth_user_id):
        
    for channel in channels_list:
        if channels_list[channel]['channel_id'] == channel_id:
            return True
    
    return False



def channel_join_v1(auth_user_id, channel_id):

    '''
    #Given a channel_id of a channel that the authorised user can join, 
    #adds them to that channel.
    #auth_user_id and channel_id are in integer form
    '''

    store = data_store.get() # get the data
    channel = channel_details_v1(auth_user_id, channel_id)

    #check if channel is valid
    if valid_channel_id(channel_id) == False:
        raise InputError("channel_id is INVALID")

    elif valid_channel_id(channel_id) == True:
        
        #check if the user is already part of the channel
        if find_user_in_channel(auth_user_id, channel_id) == True:
            raise InputError("User already in channel")    

        #check if the chanel is private and whether the user if part 
        #of the channel or not
        else:
            if channel['is_public'] == False:
            raise AccessError("This channel is PRIVATE")

    #add the user to the channel
    channel['all_members'][auth_user_id] = auth_user_id
    return {
    }

