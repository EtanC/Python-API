from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helper import token_to_user

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

    # INPUT ERROR: if any u_id in u_ids does not refer to a valid user
    if (check_valid_id(u_ids, store) == False) or len(u_ids) == 0: 
        raise InputError("Invalid u_id")
    
    # check token, if valid, the return would be 
    if token_to_user(token, store) != None: 
        owner = token_to_user(token,store)
    else: 
        raise AccessError('Invalid token')

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
        'messages' : [],
        'name' : dm_name
    }
    # Append channel_data to 'dms' list in data_store 
    store['dms'].append(dm_data)
    data_store.set(store)
    
    return {
        'dm_id': dm_id,
    }
'''

Returns the list of DMs that the user is a member of.

'''
def dm_list_v1(token): 
    store = data_store.get()

    # token validity check
    if token_to_user(token, store) != None: 
        user = token_to_user(token,store)
        # extract the u_id from the user
        u_id  = user['u_id']
    else: 
        raise AccessError('Invalid token')
    
    # user validity check
    if check_valid_id(u_id, store) == False: 
        raise InputError("Invalid u_id")
    
    dm_data = []
    # a list of dictionary that we return
    return_dms = {'dms' : dm_data}
    dm_data = []

    # check if the user'd u_id is part of the dm, 
    # if so, append it to dm_data.
    for dm_id in store['dms']: 
        for member in dm_id['members']: 
            if u_id == member['u_id']: 
                dm = {'dm_id' : dm_id['dm_id'], 'name' : dm_id['name']}
                dm_data.append(dm)

    return return_dms

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