'''
The auth module
Handles registering and logging in users.
Stores data about users when they register
'''
from src.data_store import data_store
from src.error import InputError, AccessError
import jwt
import re
import hashlib
import smtplib, ssl
import secrets
from src.config import SECRET, EMAIL_REGEX, DUMMY_EMAIL, DUMMY_PASSWORD, RESET_CODE_LENGTH
from src.helper import decode_token, get_user, current_timestamp
from PIL import Image
import os
from src import config

MIN_PASSWORD_LENGTH = 6
MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 50
STARTING_SESSION_ID = 1
STARTING_APPEND_NUMBER_HANDLE = 0

def encode_token(data):
    return jwt.encode(data, SECRET, algorithm="HS256")

def hash(string):
    return hashlib.sha256(string.encode()).hexdigest()

def verify_login(email, password, store):
    '''
    Returns the user if the email and matching password is stored
    in the system. Returns None otherwise.
    '''
    for user in store['users']:
        if email == user['email']:
            if hash(password) == user['password']:
                return user
            else:
                return None
    return None

def auth_login_v1(email, password):
    '''
    Returns the user's user id and a token for the current session if login is
    successful

    Arguments:
        email       (str)    - The email the user registered with
        password    (str)    - The password the user registered with

    Exceptions:
        InputError  - Email does not belong to any user
                    - Password is incorrect

    Return Value:
        Returns {'token' : token, 'auth_user_id' : user_id} on successful call
    '''
    store = data_store.get()
    user = verify_login(email, password, store)
    if user == None:
        raise InputError(description="Invalid email or password")
    ## TODO: write a test for logout then login
    if len(user['active_session_ids']) < 1:
        session_id = STARTING_SESSION_ID
    else:
        session_id = user['active_session_ids'][-1] + 1
    user['active_session_ids'].append(session_id)
    return {
        'token' : encode_token(
            {'auth_user_id' : user['u_id'], 'session_id' : session_id}
        ),
        'auth_user_id': user['u_id'],
    }

def valid_email(email, store):
    '''
    Checks if the email is already taken and if the email format is valid
    '''
    for user in store['users']:
        if email == user['email']:
            raise InputError(description="Email already in use")
    return bool(re.match(EMAIL_REGEX, email))

def valid_password(password):
    return len(password) >= MIN_PASSWORD_LENGTH

def valid_name(name):
    return MIN_NAME_LENGTH <= len(name) <= MAX_NAME_LENGTH

def filter_only_alphanumeric(string):
    '''
    Helper function for handle creation. Given a string, will return the
    string with only the alphanumeric characters remaining and lower cased
    '''
    return ''.join(list(filter(lambda l: l.isalnum(), string))).lower()

def handle_is_unique(handle, store):
    for user in store['users']:
        if user['handle_str'] == handle:
            return False
    return True

def handle(name_first, name_last, store):
    '''
    Returns a handle based on the first and last name provided.
    Also checks if the handle is already taken.
    If it is, will append a number to handle to make it unique.
    '''
    handle = filter_only_alphanumeric(name_first)\
             + filter_only_alphanumeric(name_last)
    # Limit handle to 20 characters
    handle = handle[:20]

    append_number = STARTING_APPEND_NUMBER_HANDLE - 1
    unique_handle = False
    # Keep increasing append number until handle is unique
    while unique_handle == False:
        unique_handle = True
        # Check if handle is taken
        if append_number != -1:
            if not handle_is_unique(handle + str(append_number), store):
                # Increment number if handle is taken
                append_number += 1
                unique_handle = False
        else:
            if not handle_is_unique(handle, store):
                # Increment number if handle is taken
                append_number += 1
                unique_handle = False
    # If number has been increased, append number to make handle unique
    if append_number != STARTING_APPEND_NUMBER_HANDLE - 1:
        handle += str(append_number)
    return handle

def auth_register_v1(email, password, name_first, name_last):
    '''
    Registers a user if email, password, name_first and name_last
    are all valid

    Arguments:
        email       (str)   - The user's email
        password    (str)   - The user's password
        name_first  (str)   - The user's first name
        name_last   (str)   - The user's last name

    Exceptions:
        InputError  - email is already in use
                    - email is not a valid email
                    - password is shorter than 6 characters
                    - name_first is not between 1-50 characters
                    - name_last is not between 1-50 characters

    Return Value:
        Returns {'token' : token, 'auth_user_id' : user_id} on successful call
    '''
    store = data_store.get()
    # Check valid email
    if valid_email(email, store) == False:
        raise InputError(description="Invalid email")
    # Check valid password
    if valid_password(password) == False:
        raise InputError(description="Password too short")
    # Check valid first name
    if valid_name(name_first) == False:
        raise InputError(description="First name must contain 1-50 characters")
    # Check valid last name
    if valid_name(name_last) == False:
        raise InputError(description="Last name must contain 1-50 characters")
    # Generate user handle
    user_handle = handle(name_first, name_last, store)
    # Store user details
    user_id = len(store['users']) + 1
    # Set permissions
    if len(store['users']) == 0:
        permission_id = 1
    else:
        permission_id = 2
    # copy default.jpg as user_id.jpg
    # store img url
    new_directory_path = os.path.join(os.getcwd(), 'images')
    default_profile = Image.open(os.path.join(new_directory_path, 'default.jpg'))
    profile_pic = default_profile.copy()
    new_image_name = f"{user_id}.jpg"
    new_image_path = os.path.join(new_directory_path, new_image_name)
    profile_pic.save(new_image_path)
    
    user = {
        'u_id' : user_id,
        'email' : email,
        'password' : hash(password),
        'name_first' : name_first,
        'name_last' : name_last,
        'handle_str' : user_handle,
        'active_session_ids' : [STARTING_SESSION_ID],
        'permission_id' : permission_id,
        'notifications' : [],
        'channels_joined' : [{
            'num_channels_joined' : 0,
            'time_stamp' : current_timestamp(),
        }],
        'dms_joined' : [{
            'num_dms_joined' : 0,
            'time_stamp' : current_timestamp(),
        }],
        'messages_sent' : [{
            'num_messages_sent' : 0,
            'time_stamp' : current_timestamp(),
        }],
        'profile_img_url': f"{config.url}user/profile/photo/{new_image_name}",
    }
    store['users'].append(user)
    data_store.set(store)
    return {
        'token' : encode_token(
            {'auth_user_id' : user_id, 'session_id' : STARTING_SESSION_ID}
        ),
        'auth_user_id': user_id,
    }

def auth_logout_v1(token):
    '''
    Given an active token, invalidates the token to log the user out.

    Arguments:
        token       (str) - token identifying user

    Exceptions:
        AccessError - Invalid token

    Return Value: 
        Returns {} on successful logout
    '''
    store = data_store.get()
    # Check valid token
    payload = decode_token(token)
    if payload is None:
        raise AccessError(description="Invalid token, payload is not valid")
    user = get_user(payload['auth_user_id'], store)
    if user is None:
        raise AccessError(description="Invalid token, user id not valid")
    if payload['session_id'] not in user['active_session_ids']:
        raise AccessError(description="Invalid token, session id not valid")
    user['active_session_ids'].remove(payload['session_id'])
    data_store.set(store)
    return {}

def generate_reset_code():
    # Specifying number of bytes, where 1 byte = 2 hex digits, so
    # reset codes can only be multiples of 2 digits long
    return secrets.token_hex(RESET_CODE_LENGTH // 2)

def auth_passwordreset_request_v1(email):
    store = data_store.get()
    target_user = None
    # Check if email is in system
    for user in store['users']:
        if user['email'] == email:
            target_user = user
    if target_user is None:
        return {}
    target_user['active_session_ids'] = []
    # Make reset_code
    reset_code = generate_reset_code()
    # Store reset_code for later use
    target_user['reset_code'] = reset_code
    # Send email with reset_code
    #-------------------------------------------------------------------
    # TODO: make sure these hard coded pieces of text go into config.py
    #-------------------------------------------------------------------
    msg = f"""\
Subject:Streams password reset

Your password reset code is: {reset_code}
If you haven't recently requested a password reset, please ignore this email
"""
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=context)
    server.login(DUMMY_EMAIL, DUMMY_PASSWORD)
    server.sendmail(DUMMY_EMAIL, email, msg)
    server.quit()
    data_store.set(store)
    return {}

def auth_passwordreset_reset_v1(reset_code, new_password):
    # Check if password is valid
    if not valid_password(new_password):
        raise InputError(description="Password too short")
    # Check if reset_code is valid
    store = data_store.get()
    target_user = None
    for user in store['users']:
        if 'reset_code' in user and user['reset_code'] == reset_code:
            target_user = user
    if target_user is None:
        raise InputError(description="Invalid reset code")
    # Invalidate the one time use reset_code, change password to new_password
    del target_user['reset_code']
    target_user['password'] = hash(new_password)
    data_store.set(store)
    return {}

