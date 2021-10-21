from src.helper import token_to_user, decode_token, valid_email
from src.error import AccessError, InputError
from src.data_store import data_store
from src.channel import get_user
from src.auth import valid_name 

def users_all_v1(token): 
    '''
    Given a user's token, return a list of all users and their associated details, 
    including: u_id, email, name_first, name_last, handle_str
    
    Arguments:
        token (str): token identifying user
        
    Exceptions: 
        AccessError - invalid token 

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
        AccessError - user1 invalid token 
    
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

def user_profile_sethandle_v1(token, handle_str): 
    '''
    Update the user's handle (display name)

    Arguments: 
        token       (str)       -   token identifying user 
        handle_str  (str)       -   handle user wants to change to 
    
    Exceptions: 
        InputError  - length of handle_str not between 3-20 chars inclusive
                    - handle_str contains non-alphanumeric chars 
                    - handle already used by another user 
        AccessError - invalid token 
    
    Return Value: 
        Returns {} on successful call 
    '''
    store = data_store.get()

    # token to user returns None if token is invalid 
    token_user = token_to_user(token, store)
    if token_user is None: 
        raise AccessError(description='Invalid token')
    
    if (len(handle_str) < 3) or (len(handle_str) > 20): 
        raise InputError(description='Handle must contain 3-20 characters')
    
    if handle_str.isalnum() == False: 
        raise InputError(description='Handle must be alphanumeric')
    
    for user in store['users']: 
        if handle_str == user['handle_str']: 
            raise InputError(description='Handle already in use')

    # by this point, handle should be within char range, alphanumeric, not used by
    # anyone else and token should be valid, so store the new handle 
    token_user['handle_str'] = handle_str 
    data_store.set(store)

    return {} 

def user_profile_setname_v1(token, name_first, name_last): 
    '''
    Update the authorised user's first and last name

    Arguments: 
        token       (str) - token identifying the user 
        name_first  (str) - first name to change to if valid
        name_last   (str) - last name to change to if valid
    
    Exceptions: 
        InputError  - length of name_first not between 1 and 50 chars inclusive
                    - length of name_last not between 1 and 50 chars inclusive
        AccessError - invalid token 
    
    Return Value: 
        Returns {} on successful call 
    '''
    store = data_store.get() 
    user = token_to_user(token, store)

    if user is None: 
        raise AccessError(description='Invalid token')

    if valid_name(name_first) == False: 
        raise InputError(description='First name must contain 1-50 characters')
    
    if valid_name(name_last) == False: 
        raise InputError(description='Last name must contain 1-50 characters')
    
    # by this point, both the first and last name should be within character range
    # so we just save them into the data_store 
    user['name_first'] = name_first
    user['name_last'] = name_last
    data_store.set(store)

    return {}  

def user_profile_setemail_v1(token, email): 
    '''
    Update the authorised user's email address 

    Arguments: 
        token (str) - token identifting user 
        email (str) - email user wants to change to if valid
    
    Exceptions: 
        InpurError  - Email entered is not in valid format 
                    - Email already used by someone else 
        AccessError - Invalid token
    
    Return Value: 
        Returns {} on successful call 
    '''
    store = data_store.get() 

    user = token_to_user(token, store)

    if user is None: 
        raise AccessError(description='Invalid token')

    # valid email will raise InputError if email is already in use 
    # return True / False based on whether email follows valid format or not 
    if valid_email(email, store) == False: 
        raise InputError(description='Invalid email format')
    
    # by this point email follows valid format and is not used by anyone else
    # so save it 
    user['email'] = email 
    data_store.set(store)

    return {}  
