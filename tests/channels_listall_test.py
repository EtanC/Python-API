import pytest

from src.channels import channels_listall_v1 as c_listall, channels_create_v1 as c_create
from src.auth import auth_register_v1, auth_login_v1 
from src.other import clear_v1
from src.error import AccessError

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
    # only has one user, logically there should not be another user with +1 auth_id
    auth_user_id = reset_data + 1
    with pytest.raises(AccessError): 
        assert c_listall(auth_user_id)

def test_empty_input1(): 
    auth_user_id = None
    with pytest.raises(AccessError): 
        assert c_listall(auth_user_id)

def test_halfEmpty_input2(): 
    auth_user_id = ""
    with pytest.raises(AccessError): 
        assert c_listall(auth_user_id)

# ===============================================================
# test_valid -> test return type is a list of dictionaries
def test_valid(reset_data): 
    auth_user_id = reset_data 
    result = c_listall(auth_user_id)
    assert type(result) is list

# when the user does not have any channels 
def test_empty_list(reset_data): 
    auth_user_id = reset_data
    assert c_listall(auth_user_id) == []

# a test where there are multiple users creating multiple channels
def test_long_list(reset_data): 
    auth_user_id = reset_data
    is_public = True

    # person 1
    email = "realemail_81@outlook.edu.au"
    password = "Password1"
    name_first = "Elon1"
    name_last = "Mask1"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # person 1 creates a channel
    user_id = result['auth_user_id']
    name = 'Elon_public1'
    c_create(user_id,name,is_public)

    # person 2
    email = "realemail_82@outlook.edu.au"
    password = "Password2"
    name_first = "Elon2"
    name_last = "Mask2"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # person 2 creates a channel
    user_id = result['auth_user_id']
    name = 'Elon_public2'
    c_create(user_id,name,is_public)

    # person 3
    email = "realemail_83@outlook.edu.au"
    password = "Password3"
    name_first = "Elon3"
    name_last = "Mask3"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # person 3 creates a channel
    user_id = result['auth_user_id']
    name = 'Elon_public3'
    c_create(user_id,name,is_public)

    # person 4
    email = "realemail_84@outlook.edu.au"
    password = "Password4"
    name_first = "Elon4"
    name_last = "Mask4"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # person 4 creates a channel
    user_id = result['auth_user_id']
    name = 'Elon_public4'
    c_create(user_id,name,is_public)

    # person 5
    email = "realemail_85@outlook.edu.au"
    password = "Password5"
    name_first = "Elon5"
    name_last = "Mask5"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # person  creates a channel
    user_id = result['auth_user_id']
    name = 'Elon_public5'
    c_create(user_id,name,is_public)
  
    assert c_listall(auth_user_id) == [
        {'channel_id': 1, 'name': 'Elon_public1'},
        {'channel_id': 2, 'name': 'Elon_public2'},
        {'channel_id': 3, 'name': 'Elon_public3'},
        {'channel_id': 4, 'name': 'Elon_public4'},
        {'channel_id': 5, 'name': 'Elon_public5'} 
    ]