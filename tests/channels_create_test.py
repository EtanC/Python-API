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
        "email": "realemail_812@outlook.edu.au", 
        "password": "Password1", 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)

    return response.json()


def test_valid(reset): 
    data_create = {
        "token": reset['token'], 
        "name": "channel1", 
        "is_public": True,
    }

    response_create = requests.post(f"{config.url}channels/create/v2",\
        json=data_create) 
    response_data = response_create.json()

    channel_id = response_data['channel_id'] 
    assert type(channel_id) is int 

def test_short_name(reset): 
    data_create = { 
        'token': reset['token'],
        'name': '', 
        'is_public': True, 
    }

    response_create = requests.post(f"{config.url}channels/create/v2",\
        json=data_create) 
    
    assert response_create.status_code == 400

def test_long_name(reset): 
    data_create = { 
        'token': reset['token'], 
        'name': 'hello'*20, 
        'is_public': True, 
    }
    
    response_create = requests.post(f"{config.url}channels/create/v2",\
        json=data_create) 
    
    assert response_create.status_code == 400 

def test_invalid_user(reset): 
    # token provided is {"name": "Kevin"}
    data_create = { 
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA', 
        'name': 'channel1', 
        'is_public': True, 
    }

    response_create = requests.post(f"{config.url}channels/create/v2",\
        json=data_create) 
    
    assert response_create.status_code == 403 

def test_stored_data(reset): 
    data_create = {
        'token': reset['token'], 
        'name': 'channel1', 
        'is_public': True, 
    }

    response = requests.post(f"{config.url}channels/create/v2", json=data_create)
    channel_id = response.json()['channel_id']

    data_details = {
        'token': reset['token'], 
        'channel_id': channel_id,
    }

    response = requests.get(f"{config.url}channel/details/v2", json=data_details)

    assert response.json() == \
    { 
        'name': 'channel1', 
        'is_public': True, 
        'owner_members': [
            { 
                'u_id': reset['auth_user_id'], 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle_str': "johnsmith"
            }
        ], 
        'all_members': [
            { 
                'u_id': reset['auth_user_id'], 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle_str': "johnsmith"
            }
        ],
    }

def test_multiple_create(reset): 

    data_create = { 
        'token': reset['token'], 
        'name': 'channel1', 
        'is_public': True, 
    }

    response = requests.post(f"{config.url}channels/create/v2", json=data_create)

    channel_id = response.json()['channel_id']
    data_create = { 
        'token': reset['token'], 
        'name': 'channel2', 
        'is_public': True, 
    }

    response = requests.post(f"{config.url}channels/create/v2", json=data_create)
    channel_id_2 = response.json()['channel_id']

    data_details = { 
        'token': reset['token'], 
        'channel_id': channel_id, 
    }

    response = requests.get(f"{config.url}channel/details/v2", json=data_details)


    assert response.json() == \
    { 
        'name': 'channel1', 
        'is_public': True, 
        'owner_members': [
            { 
                'u_id': reset['auth_user_id'], 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle_str': "johnsmith"
            }
        ], 
        'all_members': [
            { 
                'u_id': reset['auth_user_id'], 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle_str': "johnsmith"
            }
        ],
    }

    data_details = { 
        'token': reset['token'], 
        'channel_id': channel_id_2, 
    }

    response = requests.get(f"{config.url}channel/details/v2", json=data_details)

    assert response.json() == \
        { 
        'name': 'channel2', 
        'is_public': True, 
        'owner_members': [
            { 
                'u_id': reset['auth_user_id'], 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle_str': "johnsmith"
            }
        ], 
        'all_members': [
            { 
                'u_id': reset['auth_user_id'], 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle_str': "johnsmith"
            }
        ],
    }
