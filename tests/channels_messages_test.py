import pytest
import requests
from src import config
from datetime import timezone, datetime

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
    return response_register.json()

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
    return response_register2.json()

@pytest.fixture
def channel1(user1):
    data_create = {
        'token': user1['token'],
        'name': 'Channel1',
        'is_public': True,
    }
    response_create = requests.post(
        f'{config.url}channels/create/v2',
        json=data_create
    )
    channel_id = response_create.json()['channel_id']
    return {'user' : user1, 'channel_id' : channel_id}


# Testing valid 

def test_valid(reset_data, channel1):
    data_messages = {
        'token' : channel1['user']['token'],
        'channel_id' : channel1['channel_id'],
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v2',
        params=data_messages
    )
    assert response_messages.json() == {'messages' : [], 'start': 0, 'end': -1}

def test_single_message(reset_data, channel1):
    data_send_message = {
        'token' : channel1['user']['token'],
        'channel_id' : channel1['channel_id'],
        'message' : 'hi',
    }
    response_send_message = requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )
    
    data_messages = {
        'token' : channel1['user']['token'],
        'channel_id' : channel1['channel_id'],
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v2',
        params=data_messages
    )
    # Checking time stamp
    channel_messages = response_messages.json()
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    assert abs(
        channel_messages['messages'][0]['time_created'] - current_time
    ) < 2
    # Checking the rest of the return
    expected = {
        'messages' : [
            {
                'message_id' : response_send_message.json()['message_id'],
                'u_id' : channel1['user']['auth_user_id'],
                'message' : 'hi',
                'is_pinned': False            }
        ],
        'start' : 0,
        'end' : -1,
    }
    # Removing time to check separately, index of 0 as there is only 1 message
    del channel_messages['messages'][0]['time_created']
    del channel_messages['messages'][0]['reacts']
    assert channel_messages == expected

def test_pagination(reset_data, channel1):
    # Send 60 messages with 'hi'
    message_ids = []
    for _ in range(60):
        data_send_message = {
            'token' : channel1['user']['token'],
            'channel_id' : channel1['channel_id'],
            'message' : 'hi',
        }
        response_send_message = requests.post(
            f'{config.url}message/send/v1',
            json=data_send_message
        )
        message_ids.insert(0, response_send_message.json()['message_id'])
    expected = ''
    data_messages = {
        'token' : channel1['user']['token'],
        'channel_id' : channel1['channel_id'],
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v2',
        params=data_messages
    )
    expected = {
        'messages' : [],
        'start' : 0,
        'end' : 50,
    }
    channel_messages = response_messages.json()
    for i in range(50):
        # Checking time stamp for each message sent
        current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        assert abs(
            channel_messages['messages'][i]['time_created'] - current_time
        ) < 2
        # Removing time stamp cuz we already checked it
        del channel_messages['messages'][i]['time_created']
        del channel_messages['messages'][i]['reacts']
        expected['messages'].append({
            'message_id' : message_ids[i],
            'u_id' : channel1['user']['auth_user_id'],
            'message' : 'hi',
            'is_pinned': False
        })
    assert channel_messages == expected

# def test_valid_nonowner(reset_data, messages_data, extra_user):
#     pass

# Testing errors

def test_invalid_channel_id_messages(reset_data, channel1):
    data_messages = {
        'token' : channel1['user']['token'],
        'channel_id' : channel1['channel_id'] + 1,
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v2',
        params=data_messages
    )
    assert response_messages.status_code == 400

def test_invalid_start_messages(reset_data, channel1):
    data_messages = {
        'token' : channel1['user']['token'],
        'channel_id' : channel1['channel_id'],
        'start' : 1000,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v2',
        params=data_messages
    )
    assert response_messages.status_code == 400

def test_invalid_user(reset_data, channel1, user2):
    data_messages = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v2',
        params=data_messages
    )
    assert response_messages.status_code == 403

def test_invalid_user_id(reset_data, channel1):
    data_messages = {
        'token' : "INVALID_TOKEN",
        'channel_id' : channel1['channel_id'],
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v2',
        params=data_messages
    )
    assert response_messages.status_code == 403


## TODO: test edge cases for the number of messages that are returned
# Eg. does channel_messages_v1(user_id, channel_id, 1) break if it has 1 message
# message_create/send required