import pytest

from src.auth import auth_register_v1, auth_login_v1
from src.other import clear_v1
from src.error import InputError

@pytest.fixture
def reset_data():
    clear_v1()

def test_invalid_email(reset_data):
    email = "uhh, im also a real email?"
    password = "asdfghjkl"
    name_first = "Bill"
    name_last = "Thompson"
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