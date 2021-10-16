import jwt

def get_user(auth_user_id, store):
    '''
    Searches for a user in the data_store with the given user_id
    Returns None if the user was not found
    '''
    for user in store['users']:
        if auth_user_id == user['u_id']:
            return user
    return None

def get_channel(channel_id, store):
    '''
    Searches for a channel in the data_store with the given channel_id
    Returns None if the channel was not found
    '''
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return None

SECRET = "L-L>V\\y3f4]fEH\\;haf/"
def decode_token(token):
    '''
    Returns the data inside the jwt token.
    Returns none if the token is invalid
    '''
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.InvalidSignatureError:
        return None