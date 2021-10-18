from src.helper import decode_token 
from src.error import AccessError 
from src.data_store import data_store

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