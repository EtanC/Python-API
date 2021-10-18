from src.helper import token_to_user, decode_token
from src.error import AccessError, InputError
from src.data_store import data_store
from src.channel import get_user

def users_all_v1(token): 
    '''
    Given a user's token, return a list of all users and their associated details, 
    including: u_id, email, name_first, name_last, handle_str
    
    Arguments:
        token (str): token identifying user
        
    Exceptions: 
        AccessError - User not authorised 

    Returns: 
        Returns {users} on successful creation 
    '''

    token_data = decode_token(token)

    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description='Invalid token')

    auth_user_id = token_data['auth_user_id']

    store = data_store.get() 
    # check if token is valid by checking of the u_id it holds exists in the data store 
    valid_token = False
    for user in store['users']: 
        if auth_user_id == user['u_id']: 
            valid_token = True 

    if not valid_token: 
        raise AccessError(description='Invalid token')

    # if token is valid, go through every user in the data store and add their 
    # 'associated details' to the users_list in a dictionary, then return the list 
    # in json format 
    users_list = [] 
    for user in store['users']: 
        users_list.append({
            'u_id': user['u_id'], 
            'email': user['email'], 
            'name_first': user['name_first'], 
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
        })
    
    return users_list

def user_profile_v1(token, u_id): 
    '''
    For a valid user, returns information about their u_id, email, first name, 
    last name and handle_str.

    Arguments: 
        token   (str) - token idenfifying user1 (accessing the route) 
        u_id    (int) - user id of the target / user2
    
    Exceptions: 
        InputError  - u_id does not refer to a valid user2 
        AccessError - user1 not authorised 
    
    Return Value: 
        Returns user2 dictionary on successfull call 
    '''

    store = data_store.get() 
    token_user = token_to_user(token, store)
    if token_user is None: 
        raise AccessError(description='Invalid token')

    user_data = get_user(u_id, store)

    if user_data == None: 
        raise InputError(description='Invalid u_id')

    user = { 
        'u_id': user_data['u_id'], 
        'email': user_data['email'], 
        'name_first': user_data['name_first'], 
        'name_last': user_data['name_last'], 
        'handle_str': user_data['handle_str'], 
    }

    return user