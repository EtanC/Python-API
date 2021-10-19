import pytest
import requests
import json
from src.channels import channels_create_v1, channels_create_v2
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
    token = response_register.json()['token']
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
def channel1(user1):
    data_create = {
        'auth_user_id': user1,
        'name': "Channel1",
        'is_public': True,
    }
    response_create = requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    )
    channel_id = response_create.json()['channel_id']
    return {'user_id' : user1['auth_user_id'], 'channel_id' : channel_id}

#EXAMPLE:
'''
def test_invalid_email_register(reset_data):
    data_register = {
        "email": "uhh, im also a real email?",
        "password": "asdfghjkl",
        "name_first": "Bill",
        "name_last": "Thompson",
    }
    response_register = requests.post(f"{config.url}auth/register/v2",json=data_register)
    assert response_register.status_code == 400
'''

def test_invalid_length_message(reset_data): #POST

    # <1 length message
    data_register = {
        "token": "TOKEN",
        "channel_id": 0,
        "message": "",
    }
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 400

    # >1000 length message (InputError)
    data_register['message'] = 'x' * 1001
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_channelID_message(reset_data): #POST

   #  get channel_id from channels/create/v2 (returns that)

    channel_id = channels_create_v2(token, name, is_public)

    data_register = {
      "token": "TOKEN",
       "message": "valid_message",
    }
    data_register.update(channel_id) 
    data_register['channel_id'] += 1

    # invalid channel ID test (InputError)
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_token_message(reset_data): #POST
    pass

def test_nonmember_channel_message(reset_data, channel1, user2): # POST

    data_register = {
       "token": user2['token'],
       "message": "valid_message",
       "channel_id": channel1['channel_id']
    }

    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 403

def test_valid_send_message(reset_data, channel1): #POST

    data_send_message = {
       #"token": user['token'], PLACEHOLDER - token not done yet
       "message": "valid_message",
       "channel_id": channel1['channel_id']
    }

    response_send_message = requests.post(
        f"{config.url}message/send/v1",
        json=data_send_message
    )
    response_send_message_data = response_send_message.json()

    dt = datetime.now()
    time_created = dt.replace(tzinfo=timezone.utc).timestamp()

    expected = {
        'messages': [
        {
            'message_id': response_send_message_data['message_id'],
            'u_id': channel1['user_id'],
            'message': "valid_message",
            'time_created': time_created,
        }
    ], 
        'start': 0,
        'end': -1 # -1 : no more messages to load

    }

    data_details = {
        #"token": user2['token'], PLACEHOLDER - token not done yet
        'channel_id': channel1['channel_id'],
        'start': 0  # 0 = first message sent
    } 

    response_channel_messages_details = requests.get(
        f"{config.url}channel/messages/v2",
        json=data_details
    )

    assert response_channel_messages_details.json() == expected





'''
def test_heroes():
    response = requests.get(f'{BASE_URL}/heroes')
    response_data = response.json()
    assert response_data[0]['id'] == 0
    assert response_data[0]['name'] == "Superman"
'''


'''
message/send/v1: POST
    Input error:
    -channel_id does not refer to a valid channel
    -length of message is <1 or >1000 characters

    Access error:
    -channel_id is valid and the authorised user 
    is not a member of the channel
'''
'''
message/edit/v1:
    Input error:
    -length of message is over 1000 characters
    -message_id does not refer to a valid message within 
    a channel/DM that the authorised user has joined

    Access error:
    -message_id refers to a valid message in a 
    joined channel/DM and none of the following are true:
        .the message was sent by the authorised user making this request
        .the authorised user has owner permissions in the channel/DM

'''



