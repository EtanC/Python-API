import requests
import pytest
from src import config

@pytest.fixture
def reset(): 
    requests.delete(f"{config.url}clear/v1")

    data_register = {
        "email" : "realemail_812@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "John",
        "name_last" : "Smith",
    }
    response = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    return response.json()

@pytest.fixture 
def create_dm(reset): 
    data_register = {
        "email" : "realemail_1@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Sam",
        "name_last" : "Smith",
    }
    person2 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id = person2.json()['auth_user_id']

    data = {
        'token': reset['token'],
        'u_ids': [u_id]
    }
    requests.get(
        f"{config.url}dm/create/v1", 
        params=data
    )
    return person2.json()


def test_return_type(reset): 
    data = {
        'token' : reset['token']
    }
    response = requests.get(
        f"{config.url}dm/list/v1", 
        params=data
    )

    assert type(response.json()) is dict


def test_invalid_token(reset): 
    data = {
        'token' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA',
    }
    response = requests.get(
        f"{config.url}dm/list/v1", 
        params=data
    )

    #inputerror 
    assert response.status_code == 403


def test_no_dm(reset): 
    data = {
        'token': reset['token']
    }
    response = requests.get(
        f"{config.url}dm/list/v1", 
        params=data
    )
    assert response.json() == \
        {
            'dms' : [
                {'dm_id': 0,'dm_name':None}
            ]
        }


def test_short(create_dm): 
    data = {
        'token' : create_dm['token']
    }
    response = requests.get(
        f"{config.url}dm/list/v1", 
        params=data
    )

    assert response.json() == \
        {
            'dms' : [
                {'dm_id': 1,'dm_name':'samsmith'}
            ]
        }


def test_long(create_dm): 
    # owner 2
    data_register = {
        "email" : "realemail_2@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Beta",
        "name_last" : "Smith",
    }
    owner2 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id = create_dm['auth_user_id']

    data = {
        'token': owner2['token'],
        'u_ids': [u_id]
    }
    requests.get(
        f"{config.url}dm/create/v1", 
        params=data
    )

    # owner 3
    data_register = {
        "email" : "realemail_3@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Cooper",
        "name_last" : "Smith",
    }
    owner3 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id = create_dm['auth_user_id']

    data = {
        'token': owner3['token'],
        'u_ids': [u_id]
    }
    requests.get(
        f"{config.url}dm/create/v1", 
        params=data
    )

    # owner 4
    data_register = {
        "email" : "realemail_4@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Beta",
        "name_last" : "Smith",
    }
    owner4 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id = create_dm['auth_user_id']

    data = {
        'token': owner4['token'],
        'u_ids': [u_id]
    }
    requests.get(
        f"{config.url}dm/create/v1", 
        params=data
    )

    # owner 5
    data_register = {
        "email" : "realemail_5@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Beta",
        "name_last" : "Smith",
    }
    owner5 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id = create_dm['auth_user_id']

    data = {
        'token': owner5['token'],
        'u_ids': [u_id]
    }
    requests.get(
        f"{config.url}dm/create/v1", 
        params=data
    )

    # person who receives the dms
    receive_dm = {
        'token' : create_dm['token']
    }
    list_dm = requests.get(
        f"{config.url}dm/list/v1", 
        params=receive_dm
    )
    
    assert list_dm.json() == \
        {
            'dms': [
                {'dm_id':1, 'name': 'samsmith'},
                {'dm_id':2, 'name': 'samsmith'},
                {'dm_id':3, 'name': 'samsmith'},
                {'dm_id':4, 'name': 'samsmith'},
                {'dm_id':5, 'name': 'samsmith'}
            ]
        }