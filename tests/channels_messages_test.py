'''
from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1
import pytest
import requests
from src import config

@pytest.fixture
def reset_data():
    requests.delete(f'{config.url}clear/v1')

@pytest.fixture
def user1():
    data_register = {
        'email': 'realemail_812@outlook.edu.au',
        'password': 'Password1',
        'name_first': 'John',
        'name_last': 'Smith',
    }
    response_register = requests.post(
        f'{config.url}auth/register/v2',
        json=data_register
    )
    return response_register.json()['auth_user_id']

@pytest.fixture
def user2():
    data_register2 = {
        'email': 'realemail_127@outlook.edu.au',
        'password': 'Password1',
        'name_first': 'Smith',
        'name_last': 'John',
    }
    response_register2 = requests.post(
        f'{config.url}auth/register/v2',
        json=data_register2
    )
    return response_register2.json()['auth_user_id']

@pytest.fixture
def channel1(user1):
    data_create = {
        'auth_user_id': user1,
        'name': 'Channel1',
        'is_public': True,
    }
    response_create = requests.post(
        f'{config.url}channels/create/v2',
        json=data_create
    )
    channel_id = response_create.json()['channel_id']
    return {'user_id' : user1, 'channel_id' : channel_id}


# Testing valid 

def test_valid(reset_data, channel1):
    data_messages = {
        'auth_user_id' : channel1['user_id'],
        'channel_id' : channel1['channel_id'],
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v1',
        json=data_messages
    )
    assert response_messages.json() == {'messages' : [], 'start': 0, 'end': -1}

# def test_valid_nonowner(reset_data, messages_data, extra_user):
#     user_id = messages_data[0]
#     channel_id = messages_data[1]
#     another_user_id = extra_user
#     channel_join_v1(another_user_id, channel_id)
#     assert channel_messages_v1(another_user_id, channel_id, 0) == {'messages' : [], 'start': 0, 'end': -1}

# Testing errors

def test_invalid_channel_id_messages(reset_data, channel1):
    data_messages = {
        'auth_user_id' : channel1['user_id'],
        'channel_id' : channel1['channel_id'] + 1,
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v1',
        json=data_messages
    )
    assert response_messages.status_code == 400

def test_invalid_start_messages(reset_data, channel1):
    data_messages = {
        'auth_user_id' : channel1['user_id'],
        'channel_id' : channel1['channel_id'],
        'start' : 1000,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v1',
        json=data_messages
    )
    assert response_messages.status_code == 400

def test_invalid_user(reset_data, channel1, user2):
    data_messages = {
        'auth_user_id' : channel1['user_id'],
        'channel_id' : user2,
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v1',
        json=data_messages
    )
    assert response_messages.status_code == 403

def test_invalid_user_id(reset_data, channel1):
    data_messages = {
        'auth_user_id' : channel1['user_id'] + 1,
        'channel_id' : channel1['channel_id'],
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v1',
        json=data_messages
    )
    assert response_messages.status_code == 403


## TODO: test edge cases for the number of messages that are returned
# Eg. does channel_messages_v1(user_id, channel_id, 1) break if it has 1 message
# message_create/send required
'''