'''
The auth module
Handles registering and logging in users.
Stores data about users when they register
'''
from src.data_store import data_store
from src.error import InputError
import jwt
import re
import hashlib
from src.config import SECRET, EMAIL_REGEX

MIN_PASSWORD_LENGTH = 6
MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 50
STARTING_SESSION_ID = 1

def encode_token(data):
    return jwt.encode(data, SECRET, algorithm="HS256")

def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])

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

def handle(name_first, name_last, store):
    '''
    Returns a handle based on the first and last name provided.
    Also checks if the handle is already taken.
    If it is, will append a number to handle to make it unique.
    '''
    handle = ""
    # Append alphanumeric characters from name_first
    for letter in name_first:
        # Checking that handle is less than 20 characters
        if len(handle) < 20:
            if letter.isalnum():
                handle += letter.lower()
        else:
            break
    # Append alphanumeric characters from name_last
    for letter in name_last:
        # Checking that handle is less than 20 characters
        if len(handle) < 20:
            if letter.isalnum():
                handle += letter.lower()
        else:
            break

    append_number = -1
    for user in store['users']:
        # Check if handle is taken
        if user['handle_str'] == handle:
            # Increment number if handle is taken
            append_number += 1
    # If number has been increased, append number to make handle unique
    if append_number != -1:
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
    user = {
        'u_id' : user_id,
        'email' : email,
        'password' : hash(password),
        'name_first' : name_first,
        'name_last' : name_last,
        'handle_str' : user_handle,
        'active_session_ids' : [STARTING_SESSION_ID]
    }
    store['users'].append(user)
    data_store.set(store)
    return {
        'token' : encode_token(
            {'auth_user_id' : user_id, 'session_id' : STARTING_SESSION_ID}
        ),
        'auth_user_id': user_id,
    }
