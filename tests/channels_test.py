'''
# MEANT TO BE DELETED????

import pytest

from src.channels import channels_list_v1 as c_list, channels_listall_v1 as c_listall, channels_create_v1 
from src.data_store import data_store
from src.auth import auth_register_v1, auth_login_v1 
from src.other import clear_v1
from src.error import InputError, AccessError

# this runs before every test function.
@pytest.fixture
def reset_data():
    clear_v1()

    # creates a real user before every test after clear_v1.
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "Elon"
    name_last = "Mask"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']
    return auth_user_id



# Blackbox test for invalid input for auth_user_id
# ===============================================================
def test_invalid_id(reset_data): 
    auth_user_id = reset_data + 1
    with pytest.raises(AccessError): 
        c_list(auth_user_id)
    with pytest.raises(AccessError): 
        c_listall(auth_user_id)

def test_empty_input1(reset_data): 
    auth_user_id = None
    with pytest.raises(AccessError): 
        c_list(auth_user_id)
    with pytest.raises(AccessError): 
        c_listall(auth_user_id)

def test_halfEmpty_input2(reset_data): 
    auth_user_id = ""
    with pytest.raises(AccessError): 
        c_list(auth_user_id)
    with pytest.raises(AccessError): 
        c_listall(auth_user_id)

# ===============================================================
def test_valid_list_all(reset_data): 
    auth_user_id = reset_data
    name = 'Elon'
    is_public = True
    channel_id = channels_create_v1(auth_user_id, name, is_public)

def test_long_list(reset_data): 
    pass

def test_empty_list(reset_data): 
    pass

'''



