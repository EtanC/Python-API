import pytest

from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError

## TODO
# - handle_str (auth_register_v1)

@pytest.fixture
def reset_data():
    clear_v1()

# Black box test valid register and login (testing auth.py)

def test_valid(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    result = auth_register_v1(email, password, name_first, name_last)
    assert auth_login_v1(email, password) == result

def test_valid_multiple_register(reset_data):
    # Details for person 1
    email1 = "realemail_812@outlook.edu.au"
    password1 = "Password1"
    name_first = "John"
    name_last = "Smith"
    result1 = auth_register_v1(email1, password1, name_first, name_last)
    # Details for person 2
    email2 = "realemail_318@outlook.edu.au"
    password2 = "Password1"
    name_first = "Bob"
    name_last = "Johnson"
    result2 = auth_register_v1(email2, password2, name_first, name_last)
    # Details for person 3
    email3 = "realemail_172@outlook.edu.au"
    password3 = "Password1"
    name_first = "Bill"
    name_last = "Smith"
    result3 = auth_register_v1(email3, password3, name_first, name_last)

    assert auth_login_v1(email1, password1) == result1
    assert auth_login_v1(email2, password2) == result2
    assert auth_login_v1(email3, password3) == result3

# Testing handle_str

def test_handle_str(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    user_id = auth_register_v1(email, password, name_first, name_last)['auth_user_id']
    channel_id = channels_create_v1(user_id, "channel_name", is_public=True)['channel_id']
    expected = {
        'name' : "channel_name",
        'is_public' : True,
        'owner_members' : [
            {
                'u_id' : user_id,
                'email' : "realemail_812@outlook.edu.au",
                'name_first' : "John",
                'name_last' : "Smith",
                'handle' : "johnsmith"
            },
        ],
        'all_members' : [
            {
                'u_id' : user_id,
                'email' : "realemail_812@outlook.edu.au",
                'name_first' : "John",
                'name_last' : "Smith",
                'handle' : "johnsmith"
            },
        ],
    }
    assert channel_details_v1(user_id, channel_id) == expected

# Tests for error checking auth_register

def test_invalid_email(reset_data):
    email = "uhh, im also a real email?"
    password = "asdfghjkl"
    name_first = "Bill"
    name_last = "Thompson"
    with pytest.raises(InputError):
        auth_register_v1(email, password, name_first, name_last)

def test_email_repeat(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    with pytest.raises(InputError):
        auth_register_v1(email, password, name_first, name_last)

def test_short_password(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "short"
    name_first = "John"
    name_last = "Smith"
    with pytest.raises(InputError):
        auth_register_v1(email, password, name_first, name_last)

def test_long_firstname(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John" * 20
    name_last = "Smith"
    with pytest.raises(InputError):
        auth_register_v1(email, password, name_first, name_last)

def test_long_lastname(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith" * 20
    with pytest.raises(InputError):
        auth_register_v1(email, password, name_first, name_last)

# Test for error checking auth_login

def test_wrong_password(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    
    password = "wrong_password"
    with pytest.raises(InputError):
        auth_login_v1(email, password)

def test_wrong_email(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    
    email = "wrong_email@outlook.com"
    with pytest.raises(InputError):
        auth_login_v1(email, password)