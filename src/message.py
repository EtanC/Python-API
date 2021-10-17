from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from json import dumps
from flask import Flask, request
from src.helper import token_to_user, get_channel


def message_send_v1(token, channel_id, message):

    

    store = data_store.get()
    channel = get_channel(channel_id, store)
    
    #checks the token's validity
    user = token_to_user(token, store)
    if user == None:
        raise AccessError(description="INVALID token passed in")



    raise InputError(description="message is TOO SHORT or TOO LONG")
    raise InputError(description="channel_id is INVALID")
    raise AccessError(description="This user is NOT part of channel")

    return {
        'message_id': message_id
    }





def message_edit_v1(token, message_id, message):
    pass
def message_remove_v1(token, message_id):
    pass
def message_senddm_v1(token, dm_id, message):
    pass



