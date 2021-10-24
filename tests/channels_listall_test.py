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
        f"{config.url}channels/listall/v2",
        params=data
    )
    response_data = response.json()

    assert type(response_data) is dict
    

def test_no_channel(reset_data): 
    user_data = {
        'token': reset_data['token'], 
    }
    listall_response = requests.get(
        f"{config.url}channels/listall/v2",
        params=user_data
    )
    assert listall_response.json() == \
    {
        'channels' : []
    }


def test_invalid_user(reset_data): 
    # create channel
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
        'token' :'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA'
    }
    response = requests.get(
        f"{config.url}channels/listall/v2",
        params=data
    )

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

    user_data = {
        'token': reset_data['token'], 
    }
    listall_response = requests.get(
        f"{config.url}channels/listall/v2",
        params=user_data
    )

    assert listall_response.json() == \
    {
        'channels' : [ 
            {
                'channel_id': 1, 
                'name': 'channel1'
            }
        ]
    }


def test_long(): 
    requests.delete(f"{config.url}clear/v1")

    # person 1
    data_register = {
        "email" : "realemail_1@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "John",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_login = { 
        "email": "realemail_1@outlook.edu.au", 
        "password": "Password1", 
    }
    response1 = requests.post(
        f'{config.url}auth/login/v2',
        json=data_login
    )
    data1 = response1.json()
    data_create = {
        "token": data1['token'], 
        "name": "channel1", 
        "is_public": True,
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    ) 

    # person 2
    data_register = {
        "email" : "realemail_2@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Sina",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_login = { 
        "email": "realemail_2@outlook.edu.au", 
        "password": "Password1", 
    }
    response2 = requests.post(
        f'{config.url}auth/login/v2',
        json=data_login
    )
    data2 = response2.json()
    data_create = {
        "token": data2['token'], 
        "name": "channel2", 
        "is_public": True,
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    ) 

    # person 3
    data_register = {
        "email" : "realemail_3@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "James",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_login = { 
        "email": "realemail_3@outlook.edu.au", 
        "password": "Password1", 
    }
    response3 = requests.post(
        f'{config.url}auth/login/v2',
        json=data_login
    )
    data3 = response3.json()
    data_create = {
        "token": data3['token'], 
        "name": "channel3", 
        "is_public": True,
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    ) 

     # person 4
    data_register = {
        "email" : "realemail_4@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Xinzhao",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_login = { 
        "email": "realemail_4@outlook.edu.au", 
        "password": "Password1", 
    }
    response4 = requests.post(
        f'{config.url}auth/login/v2',
        json=data_login
    )
    data4 = response4.json()
    data_create = {
        "token": data4['token'], 
        "name": "channel4", 
        "is_public": True,
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    ) 

    # person 5
    data_register = {
        "email" : "realemail_5@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "Ethan",
        "name_last" : "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_login = { 
        "email": "realemail_5@outlook.edu.au", 
        "password": "Password1", 
    }
    response5 = requests.post(
        f'{config.url}auth/login/v2',
        json=data_login
    )
    data5 = response5.json()
    data_create = {
        "token": data5['token'], 
        "name": "channel5", 
        "is_public": True,
    }
    requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    ) 

    user_data = {
        'token': data5['token'], 
    }
    listall_response = requests.get(
        f"{config.url}channels/listall/v2",
        params=user_data
    )

    assert listall_response.json() == \
    {
        'channels' : [
            {'channel_id': 1, 'name': 'channel1'},
            {'channel_id': 2, 'name': 'channel2'},
            {'channel_id': 3, 'name': 'channel3'},
            {'channel_id': 4, 'name': 'channel4'},
            {'channel_id': 5, 'name': 'channel5'} 
        ]
    }
    
