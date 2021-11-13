import pytest
import requests
from src import message
from src.channel import channel_messages_v1
from datetime import timezone, datetime
import json
from src.channels import channels_create_v1
from src.message import message_send_v1, message_remove_v1, message_edit_v1, message_pin_v1
from datetime import timezone, datetime
from src import config
from src.channel import channel_messages_v1

'''
    port = 8080
    url = f"http://localhost:{port}/"
'''

# ONLY OWNERS CAN PIN THE MESSAGE!!
# GLOBAL OWNER??

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

@pytest.fixture
def message_to_pin(user1, channel1):
    token = user1['token']
    channel_id = channel1['channel_id']
    message = "user1_valid_message_to_pin"

    data_send_message = {
       "token": token,
       "message": message,
       "channel_id": channel_id
    }
    
    # message/send/v1
    response_send_message = requests.post(f"{config.url}message/send/v1",\
        json=data_send_message
    )
    message_id = response_send_message.json()['message_id']
    return {'message_id' : message_id , 'message' : message}

@pytest.fixture
def message_to_pin_dm(user1, dm1):
    token = user1['token']
    dm_id = dm1['dm_id']
    message = "user1_valid_dm_message_to_pin"

    data_send_message = {
       "token": token,
       "message": message,
       "dm_id": dm_id
    }
    
    # message/send/v1
    response_send_message = requests.post(f"{config.url}message/senddm/v1",\
        json=data_send_message
    )

    message_id = response_send_message.json()['message_id']
    return {'message_id' : message_id , 'message' : message}

@pytest.fixture
def other_message(user1, channel1):
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
    message_id = response_send_message.json()['message_id']
    return {'message_id' : message_id, 'message' : message}

# pin one message 
def test_valid_pin(reset_data, user1, channel1, message_to_pin): #POST

    # user1 is the owner so can pin the message
    token = user1['token']
    channel_id = channel1['channel_id']
    message_id = message_to_pin['message_id']

    data_pin_message = {
        "token": token,
        "message_id": message_id,
    }

    requests.post(f"{config.url}message/pin/v1", \
        json=data_pin_message)

    # display any pinned messages
    channel_messages = {
        "token": token,
        "channel_id": channel_id,
        "start": 0
    }

    response_channel_messages_details =requests.get(f"{config.url}channel/messages/v2", \
        params=channel_messages)

    expected_data = {
        'messages': [
            {
                'message_id': message_to_pin['message_id'],
                'u_id': channel1['user_id'],
                'message': "user1_valid_message_to_pin",
                'reacts': [{'is_this_user_reacted': False,
                            'react_id': 1,                        
                            'u_ids': []}],
                'is_pinned': True,
                
            }
        ],
        'start': 0,
        'end': -1 
    }

    dt = datetime.now()
    expected_time = dt.replace(tzinfo=timezone.utc).timestamp()
    response_data = response_channel_messages_details.json()
    messages_result = response_data['messages']
    actual_time = messages_result[0]['time_created']
    time_difference = actual_time - expected_time
    assert time_difference < 2

    del response_data['messages'][0]['time_created']
    assert response_data == expected_data

# pin one message in dm

def test_valid_pin_dm(reset_data, user1, dm1, message_to_pin_dm) : #POST:
    # user1 is the owner so can pin the message
    token = user1['token']
    dm_id = dm1['dm_id']
    message_id = message_to_pin_dm['message_id']

    data_pin_message = {
        "token": token,
        "message_id": message_id,
    }

    requests.post(f"{config.url}message/pin/v1", \
        json=data_pin_message)

    # display any pinned messages
    dm_messages = {
        "token": token,
        "dm_id": dm_id,
        "start": 0
    }

    response_dm_messages_details =requests.get(f"{config.url}dm/messages/v1", \
        params=dm_messages)

    expected_data = {
        'messages': [
            {
                'message_id': message_to_pin_dm['message_id'],
                'u_id': user1['auth_user_id'],
                'message': message_to_pin_dm['message'],
                'reacts': [{'is_this_user_reacted': False,
                            'react_id': 1,                        
                            'u_ids': []}],
                'is_pinned': True,
            }
        ],
        'start': 0,
        'end': -1 
    }

    dt = datetime.now()
    expected_time = dt.replace(tzinfo=timezone.utc).timestamp()
    response_data = response_dm_messages_details.json()


    messages_result = response_data['messages']
    actual_time = messages_result[0]['time_created']
    time_difference = actual_time - expected_time
    assert time_difference < 2

    del response_data['messages'][0]['time_created']
    assert response_data == expected_data

# pin the correct message from multiple messages
def test_valid_pin2(reset_data, user1, channel1, message_to_pin, other_message): #POST

    # user1 is the owner so can pin the message
    token = user1['token']
    channel_id = channel1['channel_id']
    message_id = message_to_pin['message_id']

    data_pin_message = {
        "token": token,
        "message_id": message_id,
    }

    requests.post(f"{config.url}message/pin/v1", \
        json=data_pin_message)

    # display any pinned messages
    channel_messages = {
        "token": token,
        "channel_id": channel_id,
        "start": 0
    }

    response_channel_messages_details =requests.get(f"{config.url}channel/messages/v2", \
        params=channel_messages)

    expected_data = {
        'messages': [
            {
                'message_id': other_message['message_id'],
                'u_id': channel1['user_id'],
                'message': other_message['message'],
                'reacts': [{'is_this_user_reacted': False,
                            'react_id': 1,                        
                            'u_ids': []}],
                'is_pinned': False,
            },

            {
                'message_id': message_to_pin['message_id'],
                'u_id': channel1['user_id'],
                'message': message_to_pin['message'],
                'reacts': [{'is_this_user_reacted': False,
                            'react_id': 1,                        
                            'u_ids': []}],
                'is_pinned': True,
            },
        
        ],
        'start': 0,
        'end': -1 
    }

    dt = datetime.now()
    expected_time = dt.replace(tzinfo=timezone.utc).timestamp()
    response_data = response_channel_messages_details.json()
    messages_result = response_data['messages']

    actual_time = messages_result[0]['time_created']
    time_difference = actual_time - expected_time
    assert time_difference < 2

    actual_time = messages_result[1]['time_created']
    time_difference = actual_time - expected_time
    assert time_difference < 2

    del response_data['messages'][0]['time_created']
    del response_data['messages'][1]['time_created']

    
    assert response_data == expected_data

# cannot pin an already pinned message
def test_invalid_already_pinned(reset_data, user1, channel1, message_to_pin):

    # user1 is the owner so can pin the message
    token = user1['token']
    message_id = message_to_pin['message_id']

    data_pin_message = {
        "token": token,
        "message_id": message_id,
    }

    requests.post(f"{config.url}message/pin/v1", \
        json=data_pin_message)

    # user1 tries to pin the message but it's already pinned
    data_pin_message = {
        "token": token,
        "message_id": message_id,
    }

    response = requests.post(f"{config.url}message/pin/v1", \
        json=data_pin_message)
    
    assert response.status_code == 400

# cannot pin an invalid message
def test_invalid_messageID(reset_data, user1, channel1, message_to_pin):

    # user1 tries to pin an invalid message (invalid ID)
    data_pin_message = {
        "token": user1['token'],
        "message_id": message_to_pin['message_id'],
    }
    data_pin_message['message_id'] += 1

    response = requests.post(f"{config.url}message/pin/v1", \
        json=data_pin_message)
    
    assert response.status_code == 400

# non-owners cannot pin messages
def test_no_owner_permissions(reset_data, user1, user2, channel1, message_to_pin):

    # get user2 to join channel1 
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }
    requests.post(
        f"{config.url}channel/join/v2", json=join_register
    )

    # user2 tries to pin a message but is NOT AN OWNER
    data_pin_message = {
        "token": user2['token'],
        "message_id": message_to_pin['message_id'],
    }

    response = requests.post(f"{config.url}message/pin/v1", \
        json=data_pin_message)
    
    assert response.status_code == 403

def test_invalid_token(reset_data, user1, channel1, message_to_pin): 

    token_register = {
        "token": "INVALID TOKEN",
        "message_id": message_to_pin['message_id'],
    }
    
    response_register = requests.post(f"{config.url}message/pin/v1",\
    json=token_register)

    assert response_register.status_code == 403


