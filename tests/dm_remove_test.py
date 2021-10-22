import requests
from src import config
import pytest

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
    response_create= requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    return (response_owner.json(), response_receiver.json(), response_create.json())

def test_return_type(reset): 
    data = {
        'token' : reset[0]['token'], 
        'dm_id' : reset[2]['dm_id']
    }
    response = requests.delete(
        f"{config.url}dm/remove/v1",
        json=data
    )
    assert type(response.json()) is dict

def test_invalid_id(reset): 
    data = {
        'token' : reset[0]['token'], 
        'dm_id' : reset[2]['dm_id'] + 1
    }
    response = requests.delete(
        f"{config.url}dm/remove/v1",
        json=data
    )
    assert response.status_code == 400

def test_Access_error(reset): 
    data = {
        'token' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA',
        'dm_id' : reset[2]['dm_id']
    }
    response = requests.delete(
        f"{config.url}dm/remove/v1",
        json=data
    )
    assert response.status_code == 403


def test_short(reset): 
    data = {
        'token' : reset[0]['token'], 
        'dm_id' : reset[2]['dm_id']
    }
    requests.delete(
        f"{config.url}dm/remove/v1",
        json=data
    )

    data = {
        'token': reset[1]['token'],
        'dm_id' : reset[2]['dm_id']
    }
    response = requests.get(
        f"{config.url}dm/details/v1",
        params=data
    )
    assert response.json() == \
        {
            'members': [],  
            'name': 'abbysmith', 
            
        }

    

def test_long(reset): 
    pass