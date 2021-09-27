import pytest

from src.channels import channels_create_v1 
from src.auth import auth_register_v1, auth_login_v1 
from src.other import clear_v1
from src.error import InputError 
from src.error import AccessError 

# Clear all data before testing 
# register and log in before testing 
@pytest.fixture 
def reset(): 
    clear_v1() 
 
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']
    return auth_user_id 

def test_valid(reset): 
    # auth_user_id = return value from reset 
    auth_user_id = reset 

    channel_name = "channel1_"
    is_public = True 
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    # take channel id from returned dictionary and check if its an int 
    channel_id = result['channel_id']
    assert type(channel_id) is int 

def test_short_name(reset): 

    auth_user_id = reset 

    channel_name = "" 
    is_public = True
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, channel_name, is_public)

def test_long_name(reset): 

    auth_user_id = reset 

    channel_name = "hello" * 20 
    is_public = True 
    with pytest.raises(InputError): 
        channels_create_v1(auth_user_id, channel_name, is_public)

def test_invalid_user(reset): 
    auth_user_id = reset + 1
    channel_name = "channel1_"
    is_public = True
    with pytest.raises(AccessError): 
        channels_create_v1(auth_user_id, channel_name, is_public)
