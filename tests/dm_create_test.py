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
    response_owner = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner
    )

    register_person = {
        "email" : "realemail_1@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Abby",
        "name_last" : "Smith",
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
        f"{config.url}dms/create/v2",
        json=data
    )
    response_data = response.json()
    assert type(response_data) is dict 


def test_inputError(reset): 
    invalid_id = 1111
    data = {
        'token' : reset[0]['token'], 
        'u_ids' : [invalid_id]
    }

    response = requests.post(
        f"{config.url}dms/create/v2",
        json=data
    )

    assert response.status_code == 403


def test_sort_name(reset): 
    register_person2 = {
        "email" : "realemail_2@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Beta",
        "name_last" : "Smith",
    }
    response_person2 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_person2
    )

    id_1 = reset[1]['auth_user_id']
    id_2 = response_person2.json()['auth_user_id']


    data = {
        'token' : reset[0], 
        'u_ids' : [id_1, id_2]
    }
    response = requests.post(
        f"{config.url}dms/create/v2",
        json=data
    )
    response_data = response.json()
    assert response_data == \
        {
            'dm_id' : 1,
            'name' : ['AbbySmith, BetaSmith']
        }


def test_owner(reset): 
    data = {
        'token' : reset[0], 
        'u_ids' : reset[1]['auth_user_id']
    }

    response = requests.post(
        f"{config.url}dms/create/v2",
        json=data
    )
    assert response == \
        {
            'owner': 'JohnSmith'
        }


def test_multiple(reset): 
    # Person 1
    id_1 = reset[1]['auth_user_id']

    # Person 2
    register_person2 = {
        "email" : "realemail_2@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Beta",
        "name_last" : "Smith",
    }
    response_person2 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_person2
    )
    id_2 = response_person2.json()['auth_user_id']

    # Person 3
    register_person3 = {
        "email" : "realemail_3@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Cope",
        "name_last" : "Smith",
    }
    response_person3 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_person3
    )
    id_3 = response_person3

    # Person 4
    register_person4 = {
        "email" : "realemail_4@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Delta",
        "name_last" : "Smith",
    }
    response_person4 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_person4
    )
    id_4 = response_person4 

    # Person 5
    register_person5 = {
        "email" : "realemail_5@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Eppa",
        "name_last" : "Smith",
    }
    response_person5 = requests.post(
        f"{config.url}auth/register/v2",
        json=register_person5
    )
    id_5 = response_person5

    data = {
        'token' : reset[0], 
        'u_ids' : [id_1,id_2,id_3,id_4,id_5]
    }
    response = requests.post(
        f"{config.url}dms/create/v2",
        json=data
    )
    assert response == \
    {
        'dm_id' : 1,
        'name' : ['AbbySmith, BetaSmith, CopeSmith, DeltaSmith, EppaSmith'],
        'owner': 'JohnSmith'
    }



