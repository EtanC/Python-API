import requests
import pytest
from src import config


@pytest.fixture
def reset(): 
    requests.delete(f"{config.url}clear/v1")


@pytest.fixture
def create_dm(): 
    # owner of dm
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

    # receiver of dm
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

    # creates the dm
    data = {
        'token' : response_owner.json()['token'], 
        'u_ids' : [u_id]
    }
    response_create = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )

    # sends dm
    data = {
        'token' : response_owner.json()['token'], 
        'dm_id' : response_create.json()['dm_id'], 
        'message' : 'Hi how are you'
    }
    response_dm = requests.post(
        f"{config.url}message/senddm/v1",
        json=data
    )

    return response_owner.json(), response_receiver.json(), response_create.json(), response_dm.json()


def test_invalid_token(reset,create_dm): 
    data = {
        'token' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA',
        'message_id' : create_dm[3]['message_id'],
        'react_id' : 1
    }
    response = requests.post(
        f"{config.url}message/react/v1",
        json=data
    )
    assert response.status_code == 403


def test_invalid_message_id(reset,create_dm): 
    data = {
        'token' : create_dm[0]['token'],
        'message_id' : create_dm[3]['message_id']+1,
        'react_id' : 1
    }
    response = requests.post(
        f"{config.url}message/react/v1",
        json=data
    )
    assert response.status_code == 400


def test_invalid_react_id(reset,create_dm): 
    data = {
        'token' : create_dm[0]['token'],
        'message_id' : create_dm[3]['message_id'],
        'react_id' : 100
    }
    response = requests.post(
        f"{config.url}message/react/v1",
        json=data
    )
    assert response.status_code == 400


def test_return_type(reset,create_dm): 
    data = {
        'token' : create_dm[0]['token'],
        'message_id' : create_dm[3]['message_id'],
        'react_id' : 1
    }
    response = requests.post(
        f"{config.url}message/react/v1",
        json=data
    )
    assert type(response.json()) is dict


def test_already_reacted(reset,create_dm): 
    # have not previously reacted
    data = {
        'token' : create_dm[1]['token'],
        'message_id' : create_dm[3]['message_id'],
        'react_id' : 1
    }
    requests.post(
        f"{config.url}message/react/v1",
        json=data
    )
    response = requests.post(
        f"{config.url}message/react/v1",
        json=data
    )
    assert response.status_code == 400


def test_valid_dm_react(reset, create_dm): 
    data = {
        # receiver reacts to it
        'token' : create_dm[1]['token'],
        'message_id' : create_dm[3]['message_id'],
        'react_id' : 1
    }
    # react
    requests.post(
        f"{config.url}message/react/v1",
        json=data
    )
    
    data = {
        'token' : create_dm[1]['token'],
        'dm_id' : create_dm[2]['dm_id'],
        'start' : 0
    }
    response = requests.get(
        f"{config.url}dm/messages/v1",
        params=data
    )

    response = response.json()

    del response['messages'][0]['time_created']
    assert response['messages'] ==   \
        [{
            'message': 'Hi how are you', 
            'message_id': create_dm[3]['message_id'],
            'u_id': create_dm[0]['auth_user_id'],
            'reacts': [{
                'is_this_user_reacted' : True,
                'react_id' : 1,
                'u_ids': [create_dm[1]['auth_user_id']]}],
                'is_pinned' : False
        }]

def test_false_react(reset, create_dm): 
    data = {
        # receiver reacts to it
        'token' : create_dm[1]['token'],
        'message_id' : create_dm[3]['message_id'],
        'react_id' : 1
    }
    requests.post(
        f"{config.url}message/react/v1",
        json=data
    )
    
    data = {
        'token' : create_dm[0]['token'],
        'dm_id' : create_dm[2]['dm_id'],
        'start' : 0
    }
    response = requests.get(
        f"{config.url}dm/messages/v1",
        params=data
    )

    response = response.json()

    # delete the time_created because it is unnecessary
    del response['messages'][0]['time_created']
    assert response['messages'] ==   \
    [{
            'message': 'Hi how are you', 
            'message_id': create_dm[3]['message_id'],
            'u_id': create_dm[0]['auth_user_id'],
            'reacts': [{
                'is_this_user_reacted' : False,
                'react_id' : 1,
                'u_ids': [create_dm[1]['auth_user_id']]}],
            'is_pinned' : False
    }]



