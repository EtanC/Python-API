from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helper import token_to_user, decode_token

'''

{dm_create_v2}
u_ids contains the user(s) that this DM is directed to,
and will not include the creator. The creator is the owner of the DM.
name should be automatically generated based on the users that are in this DM.
The name should be an alphabetically-sorted,
comma-and-space-separated list of user handles,

'''


def dm_create_v1(token, u_ids):
    store = data_store.get()

    # check token, if valid, the return would be
    if token_to_user(token, store) is not None:
        owner = token_to_user(token, store)
    else:
        raise AccessError('Invalid token')

    # INPUT ERROR: if any u_id in u_ids does not refer to a valid user
    if (check_valid_id(u_ids, store) == False) or len(u_ids) == 0:
        raise InputError("Invalid u_id")


    # get dm_id by counting number of dm and adding one
    # assuming it starts at 1
    dm_id = len(store['dms']) + 1

    # based on user_id passed in,
    # copy creator user's dictionary into user_list
    user_list = []
    for u_id in u_ids:
        for users in store['users']:
            if u_id == users['u_id']:
                user_list.append(users)

    # sorting name in alphabetical order
    dm_name = []
    for users in user_list:
        dm_name.append(users['handle_str'])
    dm_name.sort()
    # over-writes the original list
    dm_name = ', '.join(dm_name)

    dm_data = {
        'dm_id': dm_id,
        'members': user_list,
        'owner': owner,
        'messages': [],
        'name': dm_name
    }
    # Append channel_data to 'dms' list in data_store
    store['dms'].append(dm_data)
    data_store.set(store)

    return {
        'dm_id': dm_id,
    }

def dm_details_v1(token, dm_id): 
    '''
    Given a DM with ID dm_id that the authorised user is a member of, 
    provide basic details about the DM. 

    Arguments: 
        token (str) - token of a member of the dm
        dm_id (int) - id of the dm 

    Exceptions: 
        InputError  - dm_id does not refer to a valid dm 
        AccessError - authorised user not a member of the dm
                    - user not authorised / invalid token 
                
    Return Value: 
        Returns { name , members } on successful call
    '''
    store = data_store.get()
    user = token_to_user(token, store)
    if user is None: 
        raise AccessError(description='Invalid token')
    
    # check if dm_id is within the list of dms 
    if not any(dic['dm_id'] == dm_id for dic in store['dms']): 
        raise InputError(description='Invalid dm id')
    
    token_data = decode_token(token)

    for dm in store['dms']: 
        if dm_id == dm['dm_id']: 
            specific_dm = dm 
    
    # check if user is in the dm by checking the user id in the token passed in 
    if not any(dic['u_id'] == token_data['auth_user_id'] for dic in specific_dm['members']): 
        raise AccessError(description='User not in dm')

    mem_list = []
    for member in specific_dm['members']: 
        mem_list.append({
            'u_id': member['u_id'], 
            'email': member['email'], 
            'name_first': member['name_first'], 
            'name_last': member['name_last'], 
            'handle_str': member['handle_str'], 
        })

    return {
        'name': specific_dm['name'], 
        'members': mem_list, 
    }

'''
Function that checks if the whole u_ids is valid

'''

# function to check if individual ids are valid


def check_id(u_id, store):
    result = False
    # if auth_user_id exists, return true, else return false
    for users in store['users']:
        if u_id == users['u_id']:
            result = True

    return result


def check_valid_id(u_ids, store):
    result = True
    for u_id in u_ids:
        if check_id(u_id, store) == False:
            result = False
    return result
