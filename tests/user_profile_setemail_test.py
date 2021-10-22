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
    data_setemail = {
        'token': reset['token'], 
        'email': 'niceemail@outlook.edu.au'
    }

    response = requests.put(f'{config.url}user/profile/setemail/v1', json=data_setemail)

    assert response.json() == {} 

    data_profile = { 
        'token': reset['token'], 
        'u_id': reset['auth_user_id'],
    }

    response = requests.get(f'{config.url}user/profile/v1', params=data_profile)

    assert response.json()['user'] == { 
        'u_id': reset['auth_user_id'], 
        'email': 'niceemail@outlook.edu.au', 
        'name_first': 'John', 
        'name_last': 'Smith', 
        'handle_str': 'johnsmith',
    }

def test_same_email(reset): 
    data_setemail = {
        'token': reset['token'], 
        'email': 'realemail_812@outlook.edu.au'
    }

    response = requests.put(f'{config.url}user/profile/setemail/v1', json=data_setemail)

    assert response.status_code == 400

def test_invalid_email(reset): 
    data_setemail = { 
        'token': reset['token'], 
        'email': 'this is a real email trust me bro',
    }

    response = requests.put(f'{config.url}user/profile/setemail/v1', json=data_setemail)

    assert response.status_code == 400 

def test_email_already_in_use(reset): 
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

    data_setemail = {
        'token': reset['token'], 
        'email': 'realemail_813@outlook.edu.au',
    }

    response = requests.put(f'{config.url}user/profile/setemail/v1', json=data_setemail)

    assert response.status_code == 400 

def test_invalid_token(reset): 
    data_setemail = { 
        'token': '', 
        'email': 'realemail_813@outlook.edu.au', 
    }
    
    response = requests.put(f'{config.url}user/profile/setemail/v1', json=data_setemail)
    assert response.status_code == 403
