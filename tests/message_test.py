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

@pytest.fixture
def dm1(user1, user2):

    u_ids = []
    u_ids.append(user1['auth_user_id'])
    u_ids.append(user2['auth_user_id'])

    #user1 creates a dm with user2 included
    data_create = {
        'token': user1['token'],
        'u_ids': u_ids
    }

    response_create = requests.post(
        f"{config.url}dm/create/v1",
        json=data_create
    )
    dm_id   = response_create.json()['dm_id']
    owner   = user1

    return {'dm_id' : dm_id, 'owner': owner, 'all_users': u_ids}

# message/senddm/v1 tests
def test_invalid_token_senddm(reset_data, user1, dm1): 

    token_register_send = {
        "token": "INVALID TOKEN",
        "dm_id": dm1['dm_id'],
        "message": "valid_message",
    }
    
    response_register = requests.post(f"{config.url}message/senddm/v1",\
    json=token_register_send)
    assert response_register.status_code == 403

def test_invalid_length_senddm(reset_data, user1, dm1): #POST

    # <1 length message
    data_register = {
        "token": user1['token'],
        "dm_id": dm1['dm_id'],
        "message": ""
    }
    response_register = requests.post(f"{config.url}message/senddm/v1",\
    json=data_register)
    assert response_register.status_code == 400

    # >1000 length message
    data_register['message'] = 'x' * 1001
    response_register = requests.post(f"{config.url}message/senddm/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_dmID_senddm(reset_data, user1, dm1): #POST

    data_register = {
        "token": user1['token'],
        "dm_id": dm1['dm_id'],
        "message": "valid_dm_message"
    }

    # invalid dm ID test (InputError)
    data_register['dm_id'] += 1
    response_register = requests.post(f"{config.url}message/senddm/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_non_member_senddm(reset_data, dm1, user3): #POST

    # user 3 is not a member of the DM
    data_register = {
       "token": user3['token'],
       "dm_id": dm1['dm_id'],
       "message": "valid_dm_message"
    }

    response_register = requests.post(f"{config.url}message/senddm/v1",\
    json=data_register)
    assert response_register.status_code == 403

def test_valid_senddm(reset_data, dm1, user2): #POST
   
    # user 2 is a member of the DM with user1
    data_senddm = {
       "token": user2['token'],
       "dm_id": dm1['dm_id'],
       "message": "valid_dm_message"
    }

    response_senddm = requests.post(f"{config.url}message/senddm/v1",\
    json=data_senddm)

    response_senddm_data = response_senddm.json()
    
    dt = datetime.now()
    expected_time = dt.replace(tzinfo=timezone.utc).timestamp()

    expected_data = {
        'messages': [
            {
            'message_id': response_senddm_data['message_id'],
            'u_id': user2['auth_user_id'],
            'message': "valid_dm_message",
            }
        ], 
        'start': 0,
        'end': -1 # -1 : no more messages to load
    }

    dm_messages = {
        "token": user2['token'], 
        'dm_id': dm1['dm_id'],
        'start': 0  # 0 = first message sent
    }

    response_dm_messages_details = requests.get(
    f"{config.url}dm/messages/v1",
    params=dm_messages) 

    # You can check if the timestamp is within a second or two 
    # of the time you send the request.

    response_data = response_dm_messages_details.json()
    messages_result = response_data['messages']
    actual_time = messages_result[0]['time_created']
    time_difference = actual_time - expected_time
    assert time_difference < 2
    del response_data['messages'][0]['time_created']

    assert response_data == expected_data



# message/edit/v1 tests
def test_invalid_token_edit(reset_data, user1, channel1): 

    token_register_send = {
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "message": "valid_message"
    }
    
    # message/send/v1
    response_register_send = requests.post(f"{config.url}message/send/v1",\
    json=token_register_send)

    message_id = response_register_send.json()['message_id']

    token_register_edit = {
        "token": "INVALID_TOKEN",
        "message_id": message_id,
        "message": "edited_valid_message"
    }

    # message/edit/v1
    response_register_edit = requests.put(f"{config.url}message/edit/v1",\
    json=token_register_edit)

    assert response_register_edit.status_code == 403

def test_invalid_length_edit(reset_data, user1, channel1): #PUT
    
    register_send = {
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "message": "valid_message"
    }
    
    # message/send/v1
    response_register_send = requests.post(f"{config.url}message/send/v1",\
    json=register_send)
    message_id = response_register_send.json()['message_id']

    data_register = {
        "token": user1['token'],
        "message_id": message_id,
        "message": "edited_valid_message",
    }

    # >1000 length message (InputError)
    data_register['message'] = 'x' * 1001
    response_register = requests.put(f"{config.url}message/edit/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_messageID_edit(reset_data, user1, channel1): #PUT

    register_send = {
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "message": "valid_message"
    }
    
    # message/send/v1
    response_register_send = requests.post(f"{config.url}message/send/v1",\
    json=register_send)
    message_id = response_register_send.json()['message_id']

    data_register = {
        "token": user1['token'],
        "message_id": message_id,
        "message": "edited_valid_message"
    }
    
    # invalid message ID (InputError)
    data_register['message_id'] += 1
    response_register = requests.put(f"{config.url}message/edit/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_user_message_edit(reset_data, user1, channel1, user2): #PUT

    # user1 sends a mesage in channel1
    token = user1['token']
    channel_id = channel1['channel_id']
    message = "user1_valid_message"
    data_send_message = {
       "token": token,
       "message": message,
       "channel_id": channel_id
    }

    response_send_message = requests.post(f"{config.url}message/send/v1",\
        json=data_send_message
    )
    response_send_message_data = response_send_message.json()

    # user2 tries to edit user1's message which is NOT ALLOWED
    message_id = response_send_message_data['message_id']
    edited_message = "user1_new_valid_message"

    data_edit_message = {
        "token": user2['token'],
        "message_id": message_id,
        "message": edited_message
    }

    response_edit_message = requests.put(f"{config.url}message/edit/v1",\
    json=data_edit_message)
    assert response_edit_message.status_code == 403 

def test_valid_message_edit(reset_data, user1, channel1): #PUT

    # user1 sends a mesage in channel1
    token = user1['token']
    channel_id = channel1['channel_id']
    message = "user1_valid_message"
    data_send_message = {
       "token": token,
       "message": message,
       "channel_id": channel_id
    }

    # message/send/v1
    response_send_message = requests.post(f"{config.url}message/send/v1",\
        json=data_send_message
    )
    response_send_message_data = response_send_message.json()

    dt = datetime.now()
    expected_time = dt.replace(tzinfo=timezone.utc).timestamp()

    # user1 edits the message
    message_id = response_send_message_data['message_id']
    edited_message = "user1_new_valid_message"

    data_edit_message = {
        "token": token,
        "message_id": message_id,
        "message": edited_message
    }

    #message/edit/v1
    requests.put(f"{config.url}message/edit/v1", \
        json=data_edit_message)

    #display the edited message using channel/messages/v2
    channel_messages = {
        "token": token,
        "channel_id": channel_id,
        "start": 0
    }

    response_channel_messages_data =requests.get(f"{config.url}channel/messages/v2", \
        params=channel_messages)

    response_data = response_channel_messages_data.json()
    
    messages_result = response_data['messages']
    actual_time = messages_result[0]['time_created']
    time_difference = actual_time - expected_time
    assert time_difference < 2
    del response_data['messages'][0]['time_created']

    expected_data = {
        'messages': [
            {
            'message_id': message_id,
            'u_id': channel1['user_id'],
            'message': edited_message,
            }
        ], 
        'start': 0,
        'end': -1 # -1 : no more messages to load
    }

    assert response_data == expected_data

def test_valid_message_edit_empty(reset_data, user1, channel1): #PUT

    # user1 sends a mesage in channel1
    token = user1['token']
    channel_id = channel1['channel_id']
    message = "user1_valid_message"
    data_send_message = {
       "token": token,
       "message": message,
       "channel_id": channel_id
    }

    # message/send/v1
    response_send_message = requests.post(f"{config.url}message/send/v1",\
        json=data_send_message
    )
    response_send_message_data = response_send_message.json()

    # user1 edits the message
    message_id = response_send_message_data['message_id']
    edited_message = ""

    data_edit_message = {
        "token": token,
        "message_id": message_id,
        "message": edited_message
    }

    #message/edit/v1
    requests.put(f"{config.url}message/edit/v1", \
        json=data_edit_message)

    #display the edited message using channel/messages/v2
    channel_messages = {
        "token": token,
        "channel_id": channel_id,
        "start": 0
    }

    response_channel_messages_data =requests.get(f"{config.url}channel/messages/v2", \
        params=channel_messages)

    response_data = response_channel_messages_data.json()
    

    expected_data = {
        'messages': [], 
        'start': 0,
        'end': -1 # -1 : no more messages to load
    }

    assert response_data == expected_data

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
        params=data_details)

    # You can check if the timestamp is within a second or two 
    # of the time you send the request.

    response_data = response_channel_messages_details.json()
    messages_result = response_data['messages']
    actual_time = messages_result[0]['time_created']
    time_difference = actual_time - expected_time
    assert time_difference < 2

    del response_data['messages'][0]['time_created']
    assert response_data == expected_data

