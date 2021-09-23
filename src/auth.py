from src.data_store import data_store
from src.error import InputError
import re

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def valid_email(email):
    return bool(re.match(EMAIL_REGEX, email))

def valid_password(password):
    return len(password) >= 6

def valid_name(name):
    return 1 <= len(name) <= 50

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
    return {
        'auth_user_id': 1,
    }
