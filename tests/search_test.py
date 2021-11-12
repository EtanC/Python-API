import pytest
import requests
from src import message
from src.channel import channel_messages_v1
from datetime import timezone, datetime
import json
from src.channels import channels_create_v1
from src.message import message_send_v1, message_remove_v1, message_edit_v1
from datetime import timezone, datetime
from src import config
from src.channel import channel_messages_v1

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


    data_send_message = {
       "token": user1['token'],
       "message": "before",
       "channel_id": channel_id
    }

    requests.post(f"{config.url}message/send/v1",
        json=data_send_message)

    data_send_message['message'] = "report"
    requests.post(f"{config.url}message/send/v1",
        json=data_send_message)
    
    data_send_message['message'] = "lemons"
    requests.post(f"{config.url}message/send/v1",
        json=data_send_message)
    
    data_send_message['message'] = "format"
    requests.post(f"{config.url}message/send/v1",
        json=data_send_message)


    return {'user_id' : user_id, 'channel_id' : channel_id}

@pytest.fixture
def dm1(user1, user2):

    u_ids = []
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

    dm_id = response_create.json()['dm_id']
    owner   = user1


    data_send_dm = {
       "token": user1['token'],
       "message": "factor",
       "dm_id": dm_id
    }

    requests.post(f"{config.url}message/senddm/v1",
        json=data_send_dm)

    data_send_dm['message'] = "resort"
    requests.post(f"{config.url}message/senddm/v1",
        json=data_send_dm)
    
    data_send_dm['message'] = "chickens"
    requests.post(f"{config.url}message/senddm/v1",
        json=data_send_dm)
    


    return {'dm_id' : dm_id, 'owner': owner, 'all_users': u_ids}

def test_valid_search(reset_data, channel1, dm1, user1):


    data_search = {
        'token': user1['token'],
        'query_str': "or"
    }

    response_search = requests.get(f"{config.url}search/v1", \
        params=data_search)

    expected_data_channel = {
        'messages': [
            {
                'message_id': 4,
                'u_id': channel1['user_id'],
                'message': "format",
                'reacts': [],
                'is_pinned': False,
            },
            {
                'message_id': 2,
                'u_id': channel1['user_id'],
                'message': "report",
                'reacts': [],
                'is_pinned': False,
            },
            {
                'message_id': 1,
                'u_id': channel1['user_id'],
                'message': "before",
                'reacts': [],
                'is_pinned': False,
            },   
            {
                'message_id': 5,
                'u_id': user1['auth_user_id'],
                'message': "factor",
                'reacts': [],
                'is_pinned': False,
            },
            {
                'message_id': 6,
                'u_id': user1['auth_user_id'],
                'message': "resort",
                'reacts': [],
                'is_pinned': False,
            },
        ],
    }


    dt = datetime.now()
    expected_time = dt.replace(tzinfo=timezone.utc).timestamp()
    response_data_search_channel = response_search.json()
    
    
    for message in response_data_search_channel['messages']:
        actual_time  = message['time_created']
        time_difference = actual_time - expected_time
        assert time_difference < 2
        del message['time_created']
    
    assert expected_data_channel == response_data_search_channel

def test_invalid_query_str(reset_data, channel1, user1):
   
    # <1 length message
    data_search = {
        'token': user1['token'],
        'query_str': ""
    }
    response_search = requests.get(f"{config.url}search/v1", \
        params=data_search)
    assert response_search.status_code == 400

    # >1000 length message
    data_search['query_str'] = 'x' * 1001
    response_search = requests.get(f"{config.url}search/v1", \
        params=data_search)
    assert response_search.status_code == 400

def test_invalid_token(reset_data, user1, channel1): 

    token_register = {
        "token": "INVALID TOKEN",
        "query_str": "apple",
    }
    
    response_register = requests.get(f"{config.url}search/v1",\
    params=token_register)

    assert response_register.status_code == 403

