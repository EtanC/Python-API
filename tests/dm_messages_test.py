import pytest 
import requests
from src import config 

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
    pass


def test_send_multiple(reset): 
    pass
