from src.data_store import data_store
from src.error import InputError
import re

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def verify_login(email, password):
    store = data_store.get()
    for user in store['users']:
        if email == user['email']:
            if password == user['password']:
                return user['u_id']
            else:
                return None
    return None

def auth_login_v1(email, password):
    user_id = verify_login(email, password)
    if user_id == None:
        raise InputError("Invalid email or password")
    return {
        'auth_user_id': user_id,
    }

def valid_email(email):
    store = data_store.get()
    for user in store['users']:
        if email == user['email']:
            raise InputError("Email already in use")
            # return False
    return bool(re.match(EMAIL_REGEX, email))

def valid_password(password):
    return len(password) >= 6

def valid_name(name):
    return 1 <= len(name) <= 50

def handle(name_first, name_last):
    return "handle"

def store_datastore(data, key):
    store = data_store.get()
    if key in store:
        store[key].append(data)
        data_store.set(store)


def auth_register_v1(email, password, name_first, name_last):
    # Check valid email
    if valid_email(email) == False:
        raise InputError("Invalid email")
    # Check valid password
    if valid_password(password) == False:
        raise InputError("Password too short")
    # Check valid first name
    if valid_name(name_first) == False:
        raise InputError("First name must contain 1-50 characters")
    # Check valid last name
    if valid_name(name_last) == False:
        raise InputError("Last name must contain 1-50 characters")
    # Generate user handle
    user_handle = handle(name_first, name_last)
    # Store user details
    user_id = 1
    user = {
        'u_id' : user_id,
        'email' : email,
        'password' : password,
        'name_first' : name_first,
        'name_last' : name_last,
        'handle' : user_handle,
    }
    store_datastore(user, 'users')
    return {
        'auth_user_id': user_id,
    }
