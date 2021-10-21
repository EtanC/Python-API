import requests
from src import config
import pytest 

@pytest.fixture
def reset(): 
    requests.delete(f"{config.url}clear/v1")

    register_owner = {
        "email" : "realemail_812@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "John",
        "name_last" : "Smith",
    }
    response = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner
    )

    register_person = {
         "email" : "realemail_1@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Abby",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=register_person
    )
    return (response.json()['token'])

def test_return_type(reset): 
    data = {
        'token' == reset[0], 
        'u_ids' == [2]
    }

    response = requests.post(
        f"{config.url}dms/create/v2",
        json=data
    )
    response_data = response.json()
    assert type(response_data) is dict 


def test_sort_name(reset): 
    register_person2 = {
        "email" : "realemail_2@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Beta",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=register_person2
    )

    data = {
        'token' == reset[0], 
        'u_ids' == [2,3]
    }
    response = requests.post(
        f"{config.url}dms/create/v2",
        json=data
    )
    response_data = response.json()
    assert response_data == \
        {
            'dm_id' : 1,
            'name' : 'Abby, Beta'
        }


def test_multiple(reset): 
    # Person 2
    register_person2 = {
        "email" : "realemail_2@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Beta",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=register_person2
    )

    # Person 3
    register_person3 = {
        "email" : "realemail_3@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Cope",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=register_person3
    )

    # Person 4
    register_person4 = {
        "email" : "realemail_4@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Delta",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=register_person4
    )

    # Person 5
    register_person5 = {
        "email" : "realemail_2@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Eppa",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=register_person5
    )

    data = {
        'token' == reset[0], 
        'u_ids' == [2,3]
    }



