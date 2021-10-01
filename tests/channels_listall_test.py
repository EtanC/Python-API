import pytest

from src.channels import channels_listall_v1 as c_listall, channels_create_v1 as c_create
from src.auth import auth_register_v1, auth_login_v1 
from src.other import clear_v1
from src.error import AccessError

# this runs before every test function.
@pytest.fixture
def reset_data():
    clear_v1()

@pytest.fixture
def create_and_reset():
    # creates a real user before every test after clear_v1.
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
        assert c_listall(auth_user_id)

def test_empty_input1(reset_data): 
    auth_user_id = None
    with pytest.raises(AccessError): 
        assert c_listall(auth_user_id)

def test_halfEmpty_input2(reset_data): 
    auth_user_id = ""
    with pytest.raises(AccessError): 
        assert c_listall(auth_user_id)

# ===============================================================
# test_valid -> test return type is dict
def test_valid(reset): 
    auth_user_id = reset 
    result = c_listall(auth_user_id)
    assert type(result) is dict

# when the user does not have any channels 
def test_empty_list(reset_data): 
    auth_user_id = reset_data
    assert c_listall(auth_user_id) == ()

def test_long_list(create_and_reset): 
    auth_user_id = create_and_reset()
    # creates 5 people who each create another 5 channels
    for i in range(5): 
        email = f"realemail_81{i}@outlook.edu.au"
        password = f"Password{i}"
        name_first = f"Elon{i}"
        name_last = f"Mask{i}"
        auth_register_v1(email, password, name_first, name_last)
        result = auth_login_v1(email, password) 
        # take user_id from returned dictionary 
        user_id = result['auth_user_id']
        # here they each create 5 channels
        for channels_id in range(5): 
            name = 'Elon_public'
            c_name = name + ' ' + channels_id
            is_public = True
            c_create(user_id,c_name,is_public)
    assert c_listall(auth_user_id) == {
        1: 'Elon_public 0',
        2: 'Elon_public 1',
        3: 'Elon_public 2', 
        4: 'Elon_public 3',
        5: 'Elon_public 4',  
        6: 'Elon_public 0',
        7: 'Elon_public 1',
        8: 'Elon_public 2', 
        9: 'Elon_public 3',
        10: 'Elon_public 4',
        11: 'Elon_public 0',
        12: 'Elon_public 1',
        13: 'Elon_public 2', 
        14: 'Elon_public 3',
        15: 'Elon_public 4',  
        16: 'Elon_public 0',
        17: 'Elon_public 1',
        18: 'Elon_public 2', 
        19: 'Elon_public 3',
        20: 'Elon_public 4',  
        21: 'Elon_public 0',
        22: 'Elon_public 1',
        23: 'Elon_public 2', 
        24: 'Elon_public 3',
        25: 'Elon_public 4',    
    }