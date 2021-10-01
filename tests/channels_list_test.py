import pytest

from src.channels import channels_list_v1 as c_list, channels_create_v1 as c_create
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
        assert c_list(auth_user_id)

def test_empty_input1(reset_data): 
    auth_user_id = None
    with pytest.raises(AccessError): 
        assert c_list(auth_user_id)

def test_halfEmpty_input2(reset_data): 
    auth_user_id = ""
    with pytest.raises(AccessError): 
        assert c_list(auth_user_id)

# when the user does not have any channels 
def test_empty_list(reset_data): 
    auth_user_id = reset_data
    assert c_list(auth_user_id) == {'channels':[]}

# ===============================================================
# test_valid -> test return type is a lsit of dictionaries
def test_valid(reset_data): 
    auth_user_id = reset_data 
    result = c_list(auth_user_id)
    assert type(result) is dict

# check the returned value contains channel_id and name 
def test_valid_list_all(reset_data): 
    auth_user_id = reset_data
    name = 'Elon_public'
    is_public = True
    c_create(auth_user_id, name, is_public)
    assert c_list(auth_user_id) == {
        'channels' : [ 
            {
                'channel_id': 1, 
                'name': 'Elon_public'
            }
        ]
    }
    
# when the user has joined multiple channels
def test_long_list(reset_data): 
    auth_user_id = reset_data
    is_public = True

    # person 1
    name1 = 'Elon_public0'
    c_create(auth_user_id,name1,is_public)

    # person 2
    name2 = 'Elon_public1'
    c_create(auth_user_id,name2,is_public)

    # person 3 
    name3 = 'Elon_public2'
    c_create(auth_user_id,name3,is_public)

    # person 4
    name4 = 'Elon_public3'
    c_create(auth_user_id,name4,is_public)

    # person 5
    name5 = 'Elon_public4'
    c_create(auth_user_id,name5,is_public)

    assert c_list(auth_user_id) == { 
        'channels' : [
            {'channel_id': 1, 'name': 'Elon_public0'},
            {'channel_id': 2, 'name': 'Elon_public1'},
            {'channel_id': 3, 'name': 'Elon_public2'},
            {'channel_id': 4, 'name': 'Elon_public3'},
            {'channel_id': 5, 'name': 'Elon_public4'} 
        ],
    }




