from datetime import datetime
import pytest 
import requests
from src import config 
from datetime import datetime, timezone

@pytest.fixture
def reset(): 
    requests.delete(f"{config.url}clear/v1")

    register_owner = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
        "name_first": "John",
        "name_last": "Smith",
    }
    response_owner = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner
    )

    register_receiver = {
        "email": "realemail_1@outlook.edu.au",
        "password": "Password1",
        "name_first": "Abby",
        "name_last": "Smith",
    }
    response_receiver = requests.post(
        f"{config.url}auth/register/v2",
        json=register_receiver
    )
    u_id = response_receiver.json()['auth_user_id']

    data = {
        'token' : response_owner.json()['token'], 
        'u_ids' : [u_id]
    }
    response_create = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    return response_owner.json(), response_receiver.json(), response_create.json()


def test_invalid_token(reset): 
    data = {
        'token' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA',
        'dm_id' : reset[2]['dm_id'],
        'start' : 0
    }
    response = requests.get(
        f"{config.url}dm/messages/v1",
        params=data
    )
    assert response.status_code == 403


def test_invalid_start_messages(reset): 
    data = {
        'token' : reset[0]['token'], 
        'dm_id' : reset[2]['dm_id'],
        'start' : 100
    }
    large_start = requests.get(
        f"{config.url}dm/messages/v1",
        params=data
    )

    assert large_start.status_code == 400


def test_invalid_dm_id(reset): 
    data = {
        'token' : reset[0]['token'], 
        'dm_id' : reset[2]['dm_id'] + 1,
        'start' : 0
    }
    response = requests.get(
        f"{config.url}dm/messages/v1",
        params=data
    )
    assert response.status_code == 400


def test_return_type(reset): 
    data = {
        'token' : reset[0]['token'], 
        'dm_id' : reset[2]['dm_id'],
        'start' : 0
    }
    response = requests.get(
        f"{config.url}dm/remove/v1",
        params=data
    )
    assert type(response.json()) is dict


def test_most_recent(reset):
    data = {
        'token' : reset[1]['token'], 
        'dm_id' : reset[2]['dm_id'],
        'start' : 0
    }
    response = requests.get(
        f"{config.url}dm/messages/v1",
        params=data
    )
    
    assert response.json() == {
        'messages' : [], 
        'start' : 0,
        'end' : -1
    }


def test_send_dm(reset):
    data = {
        'token' : reset[1]['token'], 
        'dm_id' : reset[2]['dm_id'],
        'message' : 'I just sent a message lol xd'
    }
    response_send = requests.post(
        f"{config.url}message/senddm/v1",
        json=data
    )

    data = {
        'token':reset[1]['token'], 
        'dm_id': reset[2]['dm_id'],
        'start': 0
    }
    response = requests.get(
        f"{config.url}dm/messages/v1",
        params=data
    )
    message = response.json()
    message_id = response_send.json()['message_id']

    # making sure that the time is within 2 seconds of each other
    time_current = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    assert abs(
        message['messages'][0]['time_created'] - time_current
    ) < 2

    del message['messages'][0]['time_created']
    del message['messages'][0]['reacts']
    assert message == \
        {
            'messages' : [{
                'message': 'I just sent a message lol xd', 
                'message_id': message_id,
                'u_id': reset[1]['auth_user_id'],
            }],
            'start' : 0,
            'end' : -1
        }


def test_multiple(reset):
    message_id = []
    for i in range(60): 
        data_send ={
            'token' : reset[1]['token'], 
            'dm_id' : reset[2]['dm_id'],
            'message' : 'I just sent a message lol xd'
        }
        response_send = requests.post(
            f"{config.url}message/senddm/v1",
            json=data_send
        )
        message_id.append(response_send.json()['message_id'])
    
    data = {
        'token':reset[1]['token'], 
        'dm_id': reset[2]['dm_id'],
        'start': 0
    }
    response_message = requests.get(
        f"{config.url}dm/messages/v1",
        params=data
    )

    expected = {
        'messages' : [],
        'start' : 0,
        'end' : 50,
    }
    message = response_message.json()

    for i in range(50):
        # making sure that the time is within 2 seconds of each other
        time_current = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        assert abs(
            message['messages'][i]['time_created'] - time_current
        ) < 2
        # remove the time stamp since we cannot test it properly
        del message['messages'][i]['time_created']
        del message['messages'][i]['reacts']

        expected['messages'].insert(0, {
            'message' : 'I just sent a message lol xd',
            'message_id': message_id[i] + 10,
            'u_id': reset[1]['auth_user_id'],
        })
    
    assert message == expected