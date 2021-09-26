from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
import pytest

@pytest.fixture
def reset_data():
    clear_v1()

# Testing valid 

def test_valid(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    user_id = auth_register_v1(email, password, name_first, name_last)
    channel_name = "Channel1"
    channel_id = channels_create_v1(user_id, channel_name, False)['channel_id']
    assert channel_messages_v1(user_id, channel_id, 0) == {'messages' : [], 'start': 0, 'end': -1}

# Testing errors

def test_invalid_channel_id(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    user_id = auth_register_v1(email, password, name_first, name_last)
    channel_name = "Channel1"
    channel_id = channels_create_v1(user_id, channel_name, False)['channel_id'] + 1
    with pytest.raises(InputError):
        channel_messages_v1(user_id, channel_id, 0)

def test_invalid_start(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    user_id = auth_register_v1(email, password, name_first, name_last)
    channel_name = "Channel1"
    channel_id = channels_create_v1(user_id, channel_name, False)
    with pytest.raises(InputError):
        channel_messages_v1(user_id, channel_id, 1000)

def test_invalid_user(reset_data):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    user_id = auth_register_v1(email, password, name_first, name_last)

    email = "realemail_127@outlook.edu.au"
    password = "Password1"
    name_first = "Smith"
    name_last = "John"
    another_user_id = auth_register_v1(email, password, name_first, name_last)
    
    channel_name = "Channel1"
    channel_id = channels_create_v1(user_id, channel_name, False)
    with pytest.raises(AccessError):
        channel_messages_v1(another_user_id, channel_id, 0)

## TODO: test edge cases for the number of messages that are returned
# Eg. does channel_messages_v1(user_id, channel_id, 1) break if it has 1 message