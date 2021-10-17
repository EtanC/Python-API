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
    '''
    data_login = { 
        "email": "realemail_812@outlook.edu.au", 
        "password": "Password1", 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)
    ''' 
    response_data = response.json()
    return response_data['token']


def test_valid(reset): 
    data_create = {
        "token": reset, 
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
        'token': reset,
        'name': '', 
        'is_public': True, 
    }

    response_create = requests.post(f"{config.url}channels/create/v2",\
        json=data_create) 
    
    assert response_create.status_code == 400

def test_long_name(reset): 
    data_create = { 
        'token': reset, 
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

# REQUIRE MORE WITH CHANNEL DETAILS
'''
def test_data_store(reset): 
    auth_user_id = reset 
    channel_name = "channel1_"
    is_public = True 
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']

    assert channel_details_v1(auth_user_id, channel_id) == \
    { 
        'name': channel_name, 
        'is_public': is_public, 
        'owner_members': [
            { 
                'u_id': auth_user_id, 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle': "johnsmith"
            }
        ], 
        'all_members': [
            { 
                'u_id': auth_user_id, 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle': "johnsmith"
            }
        ],
    }

def test_multiple_create(reset): 
    auth_user_id = reset 
    channel_name = "channel1_"
    is_public = True 
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']

    channel_name2 = "channel2" 
    result = channels_create_v1(auth_user_id, channel_name2, is_public) 
    channel_id2 = result['channel_id']

    assert channel_details_v1(auth_user_id, channel_id) == \
    { 
        'name': channel_name, 
        'is_public': is_public, 
        'owner_members': [
            { 
                'u_id': auth_user_id, 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle': "johnsmith"
            }
        ], 
        'all_members': [
            { 
                'u_id': auth_user_id, 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle': "johnsmith"
            }
        ],
    }

    assert channel_details_v1(auth_user_id, channel_id2) == \
        { 
        'name': channel_name2, 
        'is_public': is_public, 
        'owner_members': [
            { 
                'u_id': auth_user_id, 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle': "johnsmith"
            }
        ], 
        'all_members': [
            { 
                'u_id': auth_user_id, 
                'email': "realemail_812@outlook.edu.au", 
                'name_first': "John", 
                'name_last': "Smith", 
                'handle': "johnsmith"
            }
        ],
    }


'''