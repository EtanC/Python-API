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
    return response_owner.json(), response_receiver.json(), response_create.json()


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
    response_delete = requests.delete(
        f"{config.url}dm/remove/v1",
        json=data
    )
    assert response_delete.status_code == 200

    # calls dm_details, should return input error
    # invalid dm_id since it doesnt exist anymore
    data = {
        'token' : reset[1]['token'],
        'dm_id': reset[2]['dm_id']
    }
    response = requests.get(
        f"{config.url}dm/details/v1",
        params=data
    )

    assert response.status_code == 400


def test_long(reset): 
    receiver_id = reset[1]['auth_user_id']
    #owner 2
    register_owner2 = {
        "email" : "realemail_2@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Beta",
        "name_last" : "Smith",
    }
    response_owner2 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner2
    )
    # owner sends dm to receiver
    data = {
        'token' : response_owner2.json()['token'], 
        'u_ids' : [receiver_id]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id1 = response.json()['dm_id']

    #owner 3
    register_owner3 = {
        "email" : "realemail_3@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Cope",
        "name_last" : "Smith",
    }
    response_owner3 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner3
    )
    # owner sends dm to receiver
    data = {
        'token' : response_owner3.json()['token'], 
        'u_ids' : [receiver_id]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id2 = response.json()['dm_id']

    #owner 4
    register_owner4 = {
        "email" : "realemail_4@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Delta",
        "name_last" : "Smith",
    }
    response_owner4 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner4
    )
    # owner sends dm to receiver
    data = {
        'token' : response_owner4.json()['token'], 
        'u_ids' : [receiver_id]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id3 = response.json()['dm_id']

    #owner 5
    register_owner5 = {
        "email" : "realemail_5@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Eppa",
        "name_last" : "Smith",
    }
    response_owner5 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner5
    )
    # owner sends dm to receiver
    data = {
        'token' : response_owner5.json()['token'], 
        'u_ids' : [receiver_id]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id4 = response.json()['dm_id']

    # delete dm no.1 
    data = {
        'token' : reset[0]['token'],
        'dm_id' : reset[2]['dm_id']
    }
    response_delete = requests.delete(
        f"{config.url}dm/remove/v1",
        json=data
    )
    assert response_delete.status_code == 200

    # calls dm_list
    data = {
        'token': reset[1]['token']
    }
    response_list = requests.get(
        f"{config.url}dm/list/v1", 
        params=data
    )

    # calls dm_details
    data = {
        'token': reset[1]['token'],
        'dm_id': reset[2]['dm_id']
    }
    response_details = requests.get(
        f"{config.url}dm/details/v1", 
        params=data
    )
    assert response_list.json() == \
    {
        'dms': [
                {'dm_id': dm_id1, 'name': 'abbysmith'},
                {'dm_id': dm_id2, 'name': 'abbysmith'},
                {'dm_id': dm_id3, 'name': 'abbysmith'},
                {'dm_id': dm_id4, 'name': 'abbysmith'}
        ]
    } 
    assert response_details.status_code == 400