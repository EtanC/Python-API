import pytest
import requests
import json
from src.channels import channels_create_v1, channels_create_v2
from src.message import message_send_v1
from datetime import timezone, datetime

from src import config
'''
port = 8080
url = f"http://localhost:{port}/"
'''

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clearmessage/v1")

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

#message/send/v1 tests
def test_invalid_length_send(reset_data): #POST

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

def test_invalid_channelID_send(reset_data, user1, channel1): #POST

    # get channel_id from channels/create/v2 (returns as dict)
    token = user1['token']
    name = "channel_one"
    is_public = True
    channel_id = channels_create_v2(token, name, is_public)

    data_register = {
      "token": token,
       "message": "valid_message",
       "channel_id": channel_id
    }
    data_register['channel_id'] += 1

    # invalid channel ID test (InputError)
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_token_send(reset_data): #POST
    pass

def test_nonmember_channel_send(reset_data, channel1, user2): # POST

    data_register = {
       "token": user2['token'],
       "message": "valid_message",
       "channel_id": channel1['channel_id']
    }

    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 403

def test_valid_send(reset_data, channel1): #POST

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
#message/edit/v1 tests 
def test_invalid_length_edit(reset_data): #PUT
    
    # >1000 length message (InputError)
    data_register = {
        "token": "TOKEN",
        "message_id": 0,
        "message": "",
    }

    data_register['message'] = 'x' * 1001
    response_register = requests.put(f"{config.url}message/edit/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_messageID_edit(reset_data, user1, channel1): #PUT

    # get message_id from message/send/v1 (returns as dict)
    token = user1['token']
    channel_id = channel1['channel_id']
    message = "valid_message"
    message_id = message_send_v1(token, channel_id, message)

    data_register = {
        "token": token,
        "message_id": message_id,
        "message": message
    }
    data_register['message_id'] += 1

    # InputError
    response_register = requests.put(f"{config.url}message/edit/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_user_message_edit(reset_data, user1, channel1, user2): #PUT

    # message_send_v1(token, channel_id, message): return {message_id}
    # user1: return {'token' : token, 'auth_user_id' : auth_user_id}
    # channel1: return {'user_id' : user1['auth_user_id'], 'channel_id' : channel_id} 
    # user2: return {'token' : token, 'auth_user_id' : auth_user_id}

    # messageID is valid BUT:
    # the message was NOT sent by the user making the request (user2)
    # the user does not have owner permissions in the channel/DM

    # channel1 contains user1
    token = user1['token']
    channel_id = channel1['channel_id']

    data_send_message = {
      "token": token,
       "message": "valid_message",
       "channel_id": channel_id
    }

    response_send_message = requests.post(f"{config.url}message/send/v1",\
        json=data_send_message
    )
    response_send_message_data = response_send_message.json()

    token = user2['token']
    message_id = response_send_message_data['message_id']
    message = "valid_message"

    data_edit_message = {
        "token": token,
        "message_id": message_id,
        "message": message,
    }

    response_edit_message = requests.post(f"{config.url}message/edit/v1",\
    json=data_edit_message)
    assert response_edit_message.status_code == 403 

def test_non_owner_message_edit(reset_data, user1, channel1, user2): #PUT

    # add user2 to channel 1 which already has user1
    channel_id = channel1['channel_id']
    token = user2['token']
    data_register = {
        "channel_id": channel_id,
        "token": token,
    }
    requests.post(f"{config.url}channel/join/v2",\
    json=data_register)

    # ASK HOW TO CHECK THE OWNERS OF THE CHANNEL
    # might need channel/details/v2 since it includes 'owner_members'
    # in the dict

    pass

'''
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



