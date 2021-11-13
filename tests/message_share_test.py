import pytest 
import requests
from src import config 
from datetime import datetime, timezone

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clear/v1")

# User 1 (global user)
@pytest.fixture
def user1():
    user1_register = {
        'email': "john.smith@gmail.com",
        'password': "password1",
        'name_first': "John",
        'name_last': "Smith",
    }

    response_user1_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user1_register
    )

    auth_user_id = response_user1_register.json()['auth_user_id']
    token        = response_user1_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# User 2 (normal user)
@pytest.fixture
def user2():
    user2_register = {
        'email': "chris.elvin@gmail.com",
        'password': "password2",
        'name_first': "Chris",
        'name_last': "Elvin",
    }

    response_user2_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user2_register
    )

    auth_user_id = response_user2_register.json()['auth_user_id']
    token        = response_user2_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# User 3 (normal user)
@pytest.fixture
def user3():
    user3_register = {
        'email': "johnny.jacobs@gmail.com",
        'password': "password3",
        'name_first': "Johnny",
        'name_last': "Jacobs",
    }

    response_user3_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user3_register
    )

    auth_user_id = response_user3_register.json()['auth_user_id']
    token        = response_user3_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# create public channel called channel2 where user1 will be added
@pytest.fixture
def channel1(user1):

    channel1_register = {
        'token': user1['token'],
        'name': "Channel1_Public",
        'is_public': True,
    }

    response_channel1_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel1_register
    )

    channel_id = response_channel1_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

# create public channel called channel2 where user1 will be added
@pytest.fixture
def channel2(user1):

    channel2_register = {
        'token': user1['token'],
        'name': "Channel2_Public",
        'is_public': True,
    }

    response_channel2_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel2_register
    )

    channel_id = response_channel2_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

def test_valid_share():
    pass

def test_invalid_channel_and_dm():
    pass

def test_no_negative_one():
    pass

def test_invalid_message():
    pass

def test_message_too_long():
    pass

def test_user_not_in_channel():
    pass