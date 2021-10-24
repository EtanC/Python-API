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
        'token': response_owner.json()['token'],
        'u_ids': [u_id]
    }
    response_create = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    return response_owner.json(), response_receiver.json(), response_create.json()


def test_return_type(reset): 
    data = {
        'token': reset[0]['token'],
        'dm_id': reset[2]['dm_id']
    }
    response = requests.post(
        f"{config.url}dm/leave/v1",
        json=data
    )
    assert isinstance(response.json(), dict)


def test_invalid_token(reset): 
    data = {
        'token': "INVALID TOKEN",
        'dm_id': reset[2]['dm_id']
    }
    response = requests.post(
        f"{config.url}dm/leave/v1",
        json=data
    )
    assert response.status_code == 403


def test_invalid_dm_id(reset): 
    data = {
        'token': reset[0]['token'],
        'dm_id': reset[2]['dm_id'] + 1
    }
    response = requests.post(
        f"{config.url}dm/leave/v1",
        json=data
    )
    assert response.status_code == 400


def test_short(reset): 
    data = {
        'token': reset[1]['token'],
        'dm_id': reset[2]['dm_id']
    }
    requests.post(
        f"{config.url}dm/leave/v1",
        json=data
    )

    # calls for dm_details
    data = {
        'token' : reset[1]['token'], 
        'dm_id': reset[2]['dm_id']
    } 
    response_removed_user = requests.get(
        f"{config.url}dm/details/v1",
        params=data
    )
    # calls for dm_list
    data = {
        'token' : reset[1]['token']
    }
    response_list = requests.get(
        f"{config.url}dm/list/v1",
        params=data
    )
    # user has left, so no long authorised
    assert response_removed_user.status_code == 403
    assert response_list.json() == \
        {
            'dms': []
        }


def test_multiple(reset): 
    receiver_id = reset[1]['auth_user_id']
    # owner 2
    register_owner2 = {
        "email": "realemail_2@outlook.edu.au",
        "password": "Password1",
        "name_first": "Beta",
        "name_last": "Smith",
    }
    response_owner2 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner2
    )
    # owner sends dm to receiver
    data = {
        'token': response_owner2.json()['token'],
        'u_ids': [receiver_id]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id1 = response.json()['dm_id']

    # owner 3
    register_owner3 = {
        "email": "realemail_3@outlook.edu.au",
        "password": "Password1",
        "name_first": "Cope",
        "name_last": "Smith",
    }
    response_owner3 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner3
    )
    # owner sends dm to receiver
    data = {
        'token': response_owner3.json()['token'],
        'u_ids': [receiver_id]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id2 = response.json()['dm_id']

    # owner 4
    register_owner4 = {
        "email": "realemail_4@outlook.edu.au",
        "password": "Password1",
        "name_first": "Delta",
        "name_last": "Smith",
    }
    response_owner4 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner4
    )
    # owner sends dm to receiver
    data = {
        'token': response_owner4.json()['token'],
        'u_ids': [receiver_id]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id3 = response.json()['dm_id']

    # owner 5
    register_owner5 = {
        "email": "realemail_5@outlook.edu.au",
        "password": "Password1",
        "name_first": "Eppa",
        "name_last": "Smith",
    }
    response_owner5 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner5
    )
    # owner sends dm to receiver
    data = {
        'token': response_owner5.json()['token'],
        'u_ids': [receiver_id]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id4 = response.json()['dm_id']

    # leave dm_0
    data = {
        'token': reset[1]['token'],
        'dm_id': reset[2]['dm_id']
    }
    requests.post(
        f"{config.url}dm/leave/v1",
        json=data
    )
    

    # leave dm_1
    data = {
        'token': reset[1]['token'],
        'dm_id': dm_id1
    }
    requests.post(
        f"{config.url}dm/leave/v1",
        json=data
    )

    # leave dm_2
    data = {
        'token': reset[1]['token'],
        'dm_id': dm_id2
    }
    requests.post(
        f"{config.url}dm/leave/v1",
        json=data
    )

    # leave dm_3
    data = {
        'token': reset[1]['token'],
        'dm_id': dm_id3
    }
    requests.post(
        f"{config.url}dm/leave/v1",
        json=data
    )

    # leave dm_4
    data = {
        'token': reset[1]['token'],
        'dm_id': dm_id4
    }
    requests.post(
        f"{config.url}dm/leave/v1",
        json=data
    )

    # calls for dm_list
    data ={
        'token' : reset[1]['token']
    }
    response_list = requests.get(
        f"{config.url}dm/list/v1",
        params=data
    )

    # calls for dm_details
    data = {
        'token' : reset[1]['token'], 
        'dm_id': reset[2]['dm_id']
    } 
    response_removed_user = requests.get(
        f"{config.url}dm/details/v1",
        params=data
    )

    assert response_removed_user.status_code == 403
    # should return empty list
    assert response_list.json() == {'dms':[]}