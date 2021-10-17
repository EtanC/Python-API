import pytest
import requests
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

    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    data_login = { 
        'email': 'realemail_812@outlook.edu.au', 
        'password': 'Password1', 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)

    return response.json()

def test_one_valid(reset): 
    data_profile = {
        'token': reset['token'], 
        'u_id': reset['auth_user_id'], 
    } 
    response = requests.get(f'{config.url}user/profile/v1', json=data_profile)

    assert response.json() == {'user': {
        'u_id': reset['auth_user_id'], 
        'email': 'realemail_812@outlook.edu.au', 
        'name_first': 'John', 
        'name_last': 'Smith', 
        'handle_str': 'johnsmith', 
    }}

def test_two_valid(reset): 
    
    data_register = {
        "email" : "realemail_813@outlook.edu.au",
        "password" : "Password2",
        "name_first" : "Tim",
        "name_last" : "Lee",
    }

    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    data_login = { 
        'email': 'realemail_813@outlook.edu.au', 
        'password': 'Password2', 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)
    response_data = response.json()
    u_id_2 = response_data['auth_user_id']

    data_profile = { 
        'token': reset['token'], 
        'u_id': u_id_2, 
    }
    response = requests.get(f'{config.url}user/profile/v1', json=data_profile)

    assert response.json() == {
        'user': {
        'u_id': u_id_2, 
        'email': 'realemail_813@outlook.edu.au', 
        'name_first': 'Tim', 
        'name_last': 'Lee', 
        'handle_str': 'timlee'
    }
    }

def test_invalid_uid(reset): 
    data_profile = { 
        'token': reset['token'], 
        'u_id': reset['auth_user_id'] + 1, 
    }

    response = requests.get(f'{config.url}user/profile/v1', json=data_profile)

    assert response.status_code == 400 

def test_invalid_user(reset): 
    # token provided is {"name": "Kevin"}
    data_profile = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA',
        'u_id': reset['auth_user_id']
    }
    response = requests.get(f'{config.url}user/profile/v1', json=data_profile)

    assert response.status_code == 403 
