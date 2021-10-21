import pytest 
import requests
from src import config 

# this runs before every test function.
@pytest.fixture
def reset_data(): 
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
    response = requests.post(
        f'{config.url}auth/login/v2',
        json=data_login
    )

    return response.json()
   

def test_return_type(reset_data): 
    # create a channel
    data_create = {
        "token": reset_data['token'], 
        "name": "channel1", 
        "is_public": True,
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    ) 

    # list
    data = {
        'token' : reset_data['token']
    }

    response = requests.get(
        f"{config.url}channels/list/v2",
        json = data
    )
    response_data = response.json()
    
    assert type(response_data) is dict


def test_no_channel(reset_data): 
    user_data = {
        'token': reset_data['token'], 
    }
    listall_response = requests.get(
        f"{config.url}channels/list/v2",
        json=user_data
    )
    assert listall_response.json() == \
    {
        'channels' : []
    }

def test_valid_user(reset_data): 
    data_create = {
        "token": reset_data['token'], 
        "name": "channel1", 
        "is_public": True,
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    ) 
    data = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA'
    }
    response = requests.get(f"{config.url}channels/list/v2",json = data)

    assert response.status_code == 403


def test_functionality(reset_data): 
    data_create = {
        "token": reset_data['token'], 
        "name": "channel1", 
        "is_public": True,
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    ) 

    # list channels
    user_data = {
        'token': reset_data['token'], 
    }
    list_response = requests.get(
        f"{config.url}channels/list/v2", 
        json=user_data
    )
    

    assert list_response.json() == \
    {
        'channels' : [ 
            {
                'channel_id': 1, 
                'name': 'channel1'
            }
        ]
    }


def test_multiple(reset_data): 
    data1 = {
        'token': reset_data['token'], 
        'name': 'Elon_public1', 
        'is_public': True, 
    }
    requests.post(f"{config.url}channels/create/v2", json=data1)

    data2 = {
        'token': reset_data['token'], 
        'name': 'Elon_public2', 
        'is_public': True, 
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data2
    )
    
    data3 = {
        'token': reset_data['token'], 
        'name': 'Elon_public3', 
        'is_public': True, 
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data3
    )

    data4 = {
        'token': reset_data['token'], 
        'name': 'Elon_public4', 
        'is_public': True, 
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data4
    )

    data5 = {
        'token': reset_data['token'], 
        'name': 'Elon_public5', 
        'is_public': True, 
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data5
    )

    user_data = {
        'token': reset_data['token'], 
    }
    list_response = requests.get(
        f"{config.url}channels/list/v2",
        json=user_data
    )


    assert list_response.json() == \
    {
        'channels' : [
            {'channel_id': 1, 'name': 'Elon_public1'},
            {'channel_id': 2, 'name': 'Elon_public2'},
            {'channel_id': 3, 'name': 'Elon_public3'},
            {'channel_id': 4, 'name': 'Elon_public4'},
            {'channel_id': 5, 'name': 'Elon_public5'} 
        ]
    }
