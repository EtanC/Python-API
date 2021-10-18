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

def test_valid(reset): 
    data_setname = { 
        'token': reset['token'],
        'name_first': 'Tim', 
        'name_last': 'Lee', 
    }

    response = requests.put(f"{config.url}user/profile/setname/v1", json=data_setname)

    assert response.json() == {} 

    data_profile = { 
        'token': reset['token'], 
        'u_id': reset['auth_user_id'], 
    }

    response = requests.get(f"{config.url}user/profile/v1", json=data_profile)

    assert response.json() == { 
        'user': {
            'u_id': reset['auth_user_id'], 
            'email': 'realemail_812@outlook.edu.au', 
            'name_first': 'Tim', 
            'name_last': 'Lee', 
            'handle_str': 'johnsmith', 
        }
    }

def test_same_name(reset): 
    data_setname = { 
        'token': reset['token'],
        'name_first': 'John', 
        'name_last': 'Smith', 
    }

    response = requests.put(f"{config.url}user/profile/setname/v1", json=data_setname)

    assert response.json() == {} 

    data_profile = { 
        'token': reset['token'], 
        'u_id': reset['auth_user_id'], 
    }

    response = requests.get(f"{config.url}user/profile/v1", json=data_profile)

    assert response.json() == { 
        'user': {
            'u_id': reset['auth_user_id'], 
            'email': 'realemail_812@outlook.edu.au', 
            'name_first': 'John', 
            'name_last': 'Smith', 
            'handle_str': 'johnsmith', 
        }
    }

def test_short_first_name(reset): 
    data_setname = { 
        'token': reset['token'],
        'name_first': '', 
        'name_last': 'Lee', 
    }

    response = requests.put(f"{config.url}user/profile/setname/v1", json=data_setname)

    assert response.status_code == 400 

def test_short_last_name(reset): 
    data_setname = { 
        'token': reset['token'],
        'name_first': 'Tim', 
        'name_last': '', 
    }

    response = requests.put(f"{config.url}user/profile/setname/v1", json=data_setname)

    assert response.status_code == 400 

def test_long_first_name(reset): 
    data_setname = { 
        'token': reset['token'],
        'name_first': 'Tim'*50, 
        'name_last': 'Lee', 
    }

    response = requests.put(f"{config.url}user/profile/setname/v1", json=data_setname)

    assert response.status_code == 400 

def test_long_last_name(reset): 
    data_setname = { 
        'token': reset['token'],
        'name_first': 'Tim', 
        'name_last': 'Lee'*50, 
    }

    response = requests.put(f"{config.url}user/profile/setname/v1", json=data_setname)

    assert response.status_code == 400 

def test_invalid_token(reset): 
    data_setname = { 
        'token': 'invalid_token',
        'name_first': 'Tim', 
        'name_last': 'Lee', 
    }

    response = requests.put(f"{config.url}user/profile/setname/v1", json=data_setname)

    assert response.status_code == 403 