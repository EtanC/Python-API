'''
The auth module
Handles registering and logging in users.
Stores data about users when they register
'''
from src.data_store import data_store
from src.error import InputError
import re

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def verify_login(email, password):
    '''
    Returns the user's user_id if the email and matching password is stored
    in the system. Returns None otherwise.
    '''
    store = data_store.get()
    for user in store['users']:
        if email == user['email']:
            if password == user['password']:
                return user['u_id']
            else:
                return None
    return None

def auth_login_v1(email, password):
    '''
    Returns a dictionary with the user's user_id if the login is succesful.
    Raises an InputError otherwise.
    '''
    user_id = verify_login(email, password)
    if user_id == None:
        raise InputError(description="Invalid email or password")
    return {
        'auth_user_id': user_id,
    }

def valid_email(email):
    '''
    Checks if the email is already taken and if the email format is valid
    '''
    store = data_store.get()
    for user in store['users']:
        if email == user['email']:
            raise InputError(description="Email already in use")
            # return False
            # ------------------------------------------------
            # NOTE: Could also use return False here, but
            # raising error provides more context on the error
            # Might change this later
            # ------------------------------------------------
    return bool(re.match(EMAIL_REGEX, email))

def valid_password(password):
    return len(password) >= 6

def valid_name(name):
    return 1 <= len(name) <= 50

def handle(name_first, name_last):
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

    # Checking if handle is taken (using dictionary for efficiency purposes)
    store = data_store.get()
    if handle in store['handle_append_no']:
        # If handle is taken, append appropiate number, increment number by 1
        store['handle_append_no'][handle] += 1
        handle += str(store['handle_append_no'][handle] - 1)
        data_store.set(store)
    else:
        # If handle is not taken, enter handle into list of used handles
        store['handle_append_no'][handle] = 0
        data_store.set(store)
    return handle

def store_datastore(data, key):
    store = data_store.get()
    if key in store:
        store[key].append(data)
        data_store.set(store)

def get_user_id():
    store = data_store.get()
    user_id = store['user_id_number']
    store['user_id_number'] += 1
    return user_id


def auth_register_v1(email, password, name_first, name_last):
    '''
    Registers a user if email, password, name_first and name_last
    are all valid. Raises an InputError if they are not.
    The conditions being checked are:
        - email must not already be in use
        - email must be a valid email
        - password must be longer than 6 characters
        - name_first must be between 1-50 characters
        - name_last must be between 1-50 characters
    '''
    # Check valid email
    if valid_email(email) == False:
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
    user_handle = handle(name_first, name_last)
    # Store user details
    user_id = get_user_id()
    user = {
        'u_id' : user_id,
        'email' : email,
        'password' : password,
        'name_first' : name_first,
        'name_last' : name_last,
        'handle_str' : user_handle,
    }
    store_datastore(user, 'users')
    return {
        'auth_user_id': user_id,
    }
