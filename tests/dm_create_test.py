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

    register_person = {
        "email": "realemail_1@outlook.edu.au",
        "password": "Password1",
        "name_first": "Abby",
        "name_last": "Smith",
    }
    response_person = requests.post(
        f"{config.url}auth/register/v2",
        json=register_person
    )
    return (response_owner.json(), response_person.json())


def test_return_type(reset):
    data = {
        'token': reset[0]['token'],
        'u_ids': [reset[1]['auth_user_id']]
    }

    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    response_data = response.json()
    assert isinstance(response_data, dict)


def test_inputError(reset):
    invalid_id = reset[1]['auth_user_id'] + 1
    data = {
        'token': reset[0]['token'],
        'u_ids': [invalid_id]
    }

    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )

    assert response.status_code == 400


def test_empty(reset):
    register_person2 = {
        "email": "realemail_2@outlook.edu.au",
        "password": "Password1",
        "name_first": "Beta",
        "name_last": "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=register_person2
    )

    data = {
        'token': reset[0]['token'],
        'u_ids': []
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    assert response.status_code == 400


def test_invalid_token(reset): 
    data = {
        'token' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA',
        'u_ids' : []
    }
    response = requests.post(
        f"{config.url}dm/create/v1", 
        json=data
    )

    #inputerror 
    assert response.status_code == 403


def test_multiple(reset):
    data = {
        'token': reset[0]['token'],
        'u_ids': [reset[1]['auth_user_id']]
    }
    requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    
    # dm2
    register_person2 = {
        "email": "realemail_2@outlook.edu.au",
        "password": "Password1",
        "name_first": "Beta",
        "name_last": "Smith",
    }
    response_person2 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_person2
    )
    id_2 = response_person2.json()['auth_user_id']
    data = {
        'token': reset[0]['token'],
        'u_ids': [id_2]
    }
    requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )

    # dm3
    register_person3 = {
        "email": "realemail_3@outlook.edu.au",
        "password": "Password1",
        "name_first": "Coopa",
        "name_last": "Smith",
    }
    response_person3 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_person3
    )
    id_3 = response_person3.json()['auth_user_id']
    data = {
        'token': reset[0]['token'],
        'u_ids': [id_3]
    }

    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id = response.json()['dm_id']
    return_id = response.json()

    assert return_id == {'dm_id': dm_id,}


def test_names(reset):
    # person 2
    data_register = {
        "email": "realemail_2@outlook.edu.au",
        "password": "Password1",
        "name_first": "Beta",
        "name_last": "Smith",
    }
    person2 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id1 = person2.json()['auth_user_id']

    # person 3
    data_register = {
        "email": "realemail_3@outlook.edu.au",
        "password": "Password1",
        "name_first": "Cooper",
        "name_last": "Smith",
    }
    person3 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id2 = person3.json()['auth_user_id']

    # person 4
    data_register = {
        "email": "realemail_4@outlook.edu.au",
        "password": "Password1",
        "name_first": "Delta",
        "name_last": "Smith",
    }
    person4 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id3 = person4.json()['auth_user_id']

    # person 5
    data_register = {
        "email": "realemail_5@outlook.edu.au",
        "password": "Password1",
        "name_first": "Eppa",
        "name_last": "Smith",
    }
    person5 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id4 = person5.json()['auth_user_id']

    # create dm
    data = {
        # owner of dm is abby smith
        'token': reset[1]['token'],
        'u_ids': [u_id1, u_id2, u_id3, u_id4]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id = response.json()['dm_id']

    # person who receives the dms
    receive_dm = {
        'token': person2.json()['token']
    }
    list_dm = requests.get(
        f"{config.url}dm/list/v1",
        params=receive_dm
    )

    assert list_dm.json() == \
        {
            'dms': [
                {'dm_id': dm_id, 'name': 'abbysmith, betasmith, coopersmith, deltasmith, eppasmith'}
            ]
    }
