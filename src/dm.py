from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helper import token_to_user, decode_token

STARTING_DM_ID = 1

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
        raise AccessError(description='Invalid token')

    # INPUT ERROR: if any u_id in u_ids does not refer to a valid user
    if (check_valid_id(u_ids, store) == False) or len(u_ids) == 0:
        raise InputError(description='Invalid u_id')

    # new dm_id  = last dm_id + 1
    if len(store['dms']) < 1:
        dm_id = STARTING_DM_ID
    else:
        dm_id = store['dms'][-1]['dm_id'] + 1

    # based on user_id passed in,
    # copy creator user's dictionary into user_list
    # include the owner
    user_list = [owner]
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

    for users in user_list:
        if users['u_id'] != owner['u_id']:
            users['notifications'].insert(0, 
                {
                "channel_id": -1,
                "dm_id": dm_id,
                "notification_message": f'{owner["handle_str"]} added you to {dm_name}'
                }
            )

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


'''

{dm_list_v2}
Returns the list of DMs that the user is a member of.

'''


def dm_list_v1(token):
    store = data_store.get()

    # token validity check
    if token_to_user(token, store) is not None:
        user = token_to_user(token, store)
        # extract the u_id from the user
        u_id = user['u_id']
    else:
        raise AccessError(description='Invalid token')

    dm_data = []

    # check if the user'd u_id is part of the dm,
    # if so, append it to dm_data.
    for dm_id in store['dms']:
        for member in dm_id['members']:
            if u_id == member['u_id']:
                dm = {'dm_id': dm_id['dm_id'], 'name': dm_id['name']}
                dm_data.append(dm)

    # a list of dictionary that we return
    return_dms = {'dms': dm_data}

    return return_dms


'''
{dm_remove_v2}
Remove an existing DM, so all members are no longer in the DM.
This can only be done by the original creator of the DM.

'''


def dm_remove_v1(token, dm_id):
    store = data_store.get()

    if token_to_user(token, store) is not None:
        owner = token_to_user(token, store)
    else:
        raise AccessError(description='Invalid token')

    if (check_valid_dmid(dm_id, store) == False):
        raise InputError(description='Invalid dm_id')

    # find matching dm_id
    for index in range(len(store['dms'])):
        if store['dms'][index]['dm_id'] == dm_id:
            dm_index = index

    if store['dms'][dm_index]['owner'] != owner:
        raise AccessError(description='Unauthorised owner')
    else:
        del store['dms'][dm_index]
        data_store.set(store)

    return {}


'''
{dm_details_v2}
Given a DM with ID dm_id that the authorised user is a member of,
provide basic details about the DM.
'''


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
    if not any(dic['u_id'] == token_data['auth_user_id']
               for dic in specific_dm['members']):
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

{dm_messages_v2}
Given a DM with ID dm_id that the authorised user is a member of, 
return up to 50 messages between index "start" and "start + 50".
Message with index 0 is the most recent message in the DM. 
This function returns a new index "end" which is the value of "start + 50", 
or, if this function has returned the least recent messages in the DM, 
returns -1 in "end" to indicate there are no more messages to load after this return.
'''
def dm_messages_v1(token, dm_id, start): 
    store = data_store.get()
    # token check
    if token_to_user(token, store) is not None:
        user = token_to_user(token, store)
        user_id = user['u_id']
    else:
        raise AccessError(description='Invalid token')

    # check if dm_id is within the list of dms
    if (not check_valid_dmid(dm_id, store)) or (dm_id == None):
        raise InputError(description='Invalid dm_id')

    for index in range(len(store['dms'])):
        if store['dms'][index]['dm_id'] == dm_id:
            dm_index = index    

    # invalid start
    if start > len(store['dms'][dm_index]['messages']):
        raise InputError(description="Invalid start")

    # check if user is authorised 
    authorised = False
    for index in range(len(store['dms'][dm_index]['members'])):
        if store['dms'][dm_index]['members'][index] == user:
            authorised = True
            
    if not authorised: 
        raise AccessError(description='Unauthorised user')
        
    # Returning up to 50 messages
    end = start + 50
    messages = store['dms'][dm_index]['messages'][start:end]

    # react section
    for message in messages: 
        message['reacts'][0]['is_this_user_reacted'] = False
        for id in message['reacts'][0]['u_ids']: 
            if user_id == id: 
                message['reacts'][0]['is_this_user_reacted'] = True
        
    # Setting end to -1 if no more messages left
    if start + 50 > len(store['dms'][dm_index]['messages']):
        end = -1

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

'''

{dm_leave_v2}
Given a DM ID, the user is removed as a member of this DM. 
The creator is allowed to leave and the DM will still exist if this happens. 
This does not update the name of the DM.

'''


def dm_leave_v1(token,dm_id): 
    store = data_store.get()
    # token check
    if token_to_user(token, store) is not None:
        user = token_to_user(token, store)
    else:
        raise AccessError(description='Invalid token')

    # check if dm_id is within the list of dms
    if (not check_valid_dmid(dm_id, store)) :
        raise InputError(description='Invalid dm_id')

    for index in range(len(store['dms'])):
        if store['dms'][index]['dm_id'] == dm_id:
            dm_index = index

    authorised = False

    for members in store['dms'][dm_index]['members']: 
        if user == members: 
            authorised = True

    if not authorised: 
        raise AccessError(description='Invalid user')
    else: 
        # find the correct index of the user
        for index in range(len(store['dms'][dm_index]['members'])):
            if store['dms'][dm_index]['members'][index] == user:
                user_index = index
        del store['dms'][dm_index]['members'][user_index]
        data_store.set(store)

    return {}


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


def check_valid_dmid(dm_id, store):
    result = False
    for dm in store['dms']:
        if dm_id == dm['dm_id']:
            result = True
            break
    return result
