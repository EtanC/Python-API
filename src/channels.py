'''
{channels_list_v1}

No input error -> assuming that auth_user_id is always valid. 
Provide a list of all channels (and their associated details) 
that the authorised user is part of.

'''
from tests.channels_test import test_invalid_id
from src.data_store import data_store
from src.error import AccessError 

# if it is valid it shouldnt raise an error 


def channels_list_v1(auth_user_id):
    pass
    

        


'''

{channels_listall_v1}

Provide a list of all channels, including private channels, (and their associated details)

'''
def channels_listall_v1(auth_user_id):

    store = data_store.get()

    if check_valid_user_id(auth_user_id, store) == False: 
        raise AccessError("Invalid auth_user_id")
    
    # access list within channels
    channels = store['channels']

    # 
    for users in channels['u_id']: 
        if auth_user_id == users['auth_user_id']:

            return channels
            
def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }

def check_valid_user_id(auth_user_id, store): 
    result = False 

    # if auth_user_id exists, return true, else return false 
    for users in store['users']: 
        if auth_user_id == users['u_id']: 
            result = True

    return result
