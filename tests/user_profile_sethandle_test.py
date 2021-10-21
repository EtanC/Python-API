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

    response = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    return response.json()

def test_valid(reset): 
    data_sethandle = { 
        'token': reset['token'], 
        'handle_str': 'DONOTTOUCH01',
    }

    response = requests.put(f'{config.url}user/profile/sethandle/v1', json=data_sethandle)

    assert response.json() == {}

    data_profile = { 
        'token': reset['token'], 
        'u_id': reset['auth_user_id'],
    }

    response = requests.get(f'{config.url}user/profile/v1', json=data_profile)

    assert response.json()['user'] == { 
        'u_id': reset['auth_user_id'], 
        'email': 'realemail_812@outlook.edu.au', 
        'name_first': 'John',
        'name_last': 'Smith', 
        'handle_str': 'DONOTTOUCH01', 
    }

def test_valid_all_numbers(reset): 
    data_sethandle = { 
        'token': reset['token'], 
        'handle_str': '0123456789',
    }

    response = requests.put(f'{config.url}user/profile/sethandle/v1', json=data_sethandle)

    assert response.json() == {}

    data_profile = { 
        'token': reset['token'], 
        'u_id': reset['auth_user_id'],
    }

    response = requests.get(f'{config.url}user/profile/v1', json=data_profile)

    assert response.json()['user'] == { 
        'u_id': reset['auth_user_id'], 
        'email': 'realemail_812@outlook.edu.au', 
        'name_first': 'John',
        'name_last': 'Smith', 
        'handle_str': '0123456789', 
    }

def test_short_handle(reset): 
    data_sethandle = { 
        'token': reset['token'], 
        'handle_str': 'hi',
    }

    response = requests.put(f'{config.url}user/profile/sethandle/v1', json=data_sethandle)

    assert response.status_code == 400 

def test_long_handle(reset): 
    data_sethandle = { 
        'token': reset['token'], 
        'handle_str': 'DONOTTOUCH01'*20,
    }

    response = requests.put(f'{config.url}user/profile/sethandle/v1', json=data_sethandle)

    assert response.status_code == 400

def test_non_alphanumeric_handle(reset): 
    data_sethandle = { 
        'token': reset['token'], 
        'handle_str': 'DONOTTOUCH!'
    }

    response = requests.put(f'{config.url}user/profile/sethandle/v1', json=data_sethandle)

    assert response.status_code == 400 

def test_full_non_alphanumeric_handle(reset): 
    data_sethandle = { 
        'token': reset['token'], 
        'handle_str': '!@#$%^&*()!'
    }

    response = requests.put(f'{config.url}user/profile/sethandle/v1', json=data_sethandle)

    assert response.status_code == 400 

def test_handle_already_in_use(reset): 
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
    
    requests.post(f'{config.url}auth/login/v2', json=data_login)
    
    data_sethandle = { 
        'token': reset['token'], 
        'handle_str': 'timlee'
    }

    response = requests.put(f'{config.url}user/profile/sethandle/v1', json=data_sethandle)

    assert response.status_code == 400 

def test_invalid_token(reset): 
    data_sethandle = { 
        'token': '', 
        'handle_str': 'DONOTTOUCH01',
    }

    response = requests.put(f'{config.url}user/profile/sethandle/v1', json=data_sethandle)

    assert response.status_code == 403