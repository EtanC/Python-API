import pytest

from src.auth import auth_register_v1, auth_login_v1
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