import json
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
            'dms' : []
        }


def test_short(reset): 
    person = {
        "email" : "realemail_1@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Sam",
        "name_last" : "Smith",
    }
    person1 = requests.post(
        f"{config.url}auth/register/v2",
        json=person
    )
    u_id = person1.json()['auth_user_id']
    
    # owner of dm sends a dm to receiver
    data = {
        'token' : reset['token'],
        'u_ids' : [u_id]
    }
    response = requests.post(
        f"{config.url}dm/create/v1", 
        json=data
    )
    dm_id = response.json()['dm_id']

    # receiver then commands for dm/list
    receiver = person1.json()
    data = {
        'token': receiver['token']
    }
    response = requests.get(
        f"{config.url}dm/list/v1", 
        params=data
    )

    assert response.json() == \
        {
            'dms' : [
                {'dm_id': dm_id,'name':'samsmith'}
            ]
        }


def test_long(reset): 
    # person 2
    data_register = {
        "email" : "realemail_2@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Beta",
        "name_last" : "Smith",
    }
    person2 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id1 = person2.json()['auth_user_id']


    # person 3
    data_register = {
        "email" : "realemail_3@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Cooper",
        "name_last" : "Smith",
    }
    person3 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id2 = person3.json()['auth_user_id']

    # person 4
    data_register = {
        "email" : "realemail_4@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Delta",
        "name_last" : "Smith",
    }
    person4 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id3 = person4.json()['auth_user_id']

    # person 5
    data_register = {
        "email" : "realemail_5@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Eppa",
        "name_last" : "Smith",
    }
    person5 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    u_id4 = person5.json()['auth_user_id']

    # create dm
    data = {
        'token': reset['token'],
        'u_ids': [u_id1,u_id2,u_id3,u_id4]
    }
    response = requests.post(
        f"{config.url}dm/create/v1", 
        json=data
    )
    dm_id = response.json()['dm_id']

    # person who receives the dms
    receive_dm = {
        'token' : person2.json()['token']
    }
    list_dm = requests.get(
        f"{config.url}dm/list/v1", 
        params=receive_dm
    )
    
    assert list_dm.json() == \
        {
            'dms': [
                {'dm_id':dm_id, 'name': 'betasmith, coopersmith, deltasmith, eppasmith'}
            ]
        }
