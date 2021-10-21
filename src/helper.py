import jwt
import re
from src.error import InputError
from src.config import SECRET, EMAIL_REGEX

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

def get_message(message_id, store):
    '''
    Searches for the message in the data_store with the given message_id
    Returns None if the message id was not found
    '''

    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return message
    return None


def decode_token(token):
    '''
    Returns the data inside the jwt token.
    Returns none if the token is invalid
    '''
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except (jwt.InvalidSignatureError, jwt.DecodeError):
        return None

def token_to_user(token, store):
    '''
    Returns the user that the token refers to if the token is valid
    Returns none if the token is invalid
    '''
    payload = decode_token(token)
    # Invalid token or signature, return none
    if payload == None:
        return None
    user = get_user(payload['auth_user_id'], store)
    # Invalid user id, return none
    if user == None:
        return None
    # Invalid session id, return none
    if payload['session_id'] not in user['active_session_ids']:
        return None
    return user

def valid_email(email, store):
    '''
    Checks if the email is already taken and if the email format is valid
    '''
    for user in store['users']:
        if email == user['email']:
            raise InputError(description="Email already in use")
    return bool(re.match(EMAIL_REGEX, email))
