import pytest
import requests
from src import message
from src.channel import channel_messages_v1
from datetime import timezone, datetime
import json
from src.channels import channels_create_v1
from src.message import message_send_v1
from datetime import timezone, datetime
from src import config
'''
port = 8080
url = f"http://localhost:{port}/"
'''

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clear/v1")

@pytest.fixture
def user1():
    data_register = {
        'email': "harry.williams@gmail.com",
        'password': "password_harry",
        'name_first': "Harry",
        'name_last': "Williams",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    auth_user_id = response_register.json()['auth_user_id']
    token        = response_register.json()['token']
    return {'token' : token, 'auth_user_id' : auth_user_id}

@pytest.fixture
def user2():
    data_register = {
        'email': "michael.dawson1@gmail.com",
        'password': "michaeldawson",
        'name_first': "Michael",
        'name_last': "Dawson",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    auth_user_id = response_register.json()['auth_user_id']
    token = response_register.json()['token']
    return {'token' : token, 'auth_user_id' : auth_user_id}

@pytest.fixture
def user3():
    data_register = {
        'email': "josh.jenkins10@gmail.com",
        'password': "joshjenkins",
        'name_first': "Josh",
        'name_last': "Jenkins",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    auth_user_id = response_register.json()['auth_user_id']
    token = response_register.json()['token']
    return {'token' : token, 'auth_user_id' : auth_user_id}

@pytest.fixture
def channel1(user1):

    data_create = {
        'token': user1['token'],
        'name': "Channel1",
        'is_public': True,
    }
    response_create = requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    )
    channel_id = response_create.json()['channel_id']
    user_id    = user1['auth_user_id']


    return {'user_id' : user_id, 'channel_id' : channel_id}


# message/send/v1 tests
def test_invalid_token_send(reset_data, user1, channel1): 

    token_register_send = {
        "token": "INVALID TOKEN",
        "channel_id": channel1['channel_id'],
        "message": "valid_message",
    }
    
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=token_register_send)
    assert response_register.status_code == 403

def test_invalid_length_send(reset_data, user1, channel1): #POST

    # <1 length message
    data_register = {
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "message": "",
    }
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 400

    # >1000 length message
    data_register['message'] = 'x' * 1001
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_channelID_send(reset_data, user1, channel1): #POST

    data_register = {
       "token": user1['token'],
       "channel_id": channel1['channel_id'],
        "message": "valid_message"

    }
    data_register['channel_id'] += 1

    # invalid channel ID test (InputError)
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_nonmember_channel_send(reset_data, channel1, user2): # POST

    data_register = {
       "token": user2['token'],
       "message": "valid_message",
       "channel_id": channel1['channel_id']
    }

    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 403

def test_valid_send(reset_data, channel1, user1): #POST

    data_send_message = {
       "token": user1['token'],
       "message": "valid_message",
       "channel_id": channel1['channel_id']
    }

    response_send_message = requests.post(
        f"{config.url}message/send/v1",
        json=data_send_message
    )
    response_send_message_data = response_send_message.json()

    dt = datetime.now()
    expected_time = dt.replace(tzinfo=timezone.utc).timestamp()
    

    expected_data = {
        'messages': [
            {
            'message_id': response_send_message_data['message_id'],
            'u_id': channel1['user_id'],
            'message': "valid_message",
            }
        ], 
        'start': 0,
        'end': -1 # -1 : no more messages to load
    }

    data_details = {
        "token": user1['token'], 
        'channel_id': channel1['channel_id'],
        'start': 0  # 0 = first message sent
    } 

    response_channel_messages_details = requests.get(
        f"{config.url}channel/messages/v2",
        json=data_details
    )
    # You can check if the timestamp is within a second or two 
    # of the time you send the request.

    response_data = response_channel_messages_details.json()
    messages_result = response_data['messages']
    actual_time = messages_result[0]['time_created']
    time_difference = actual_time - expected_time
    assert time_difference < 2

    del response_data['messages'][0]['time_created']
    assert response_data == expected_data

