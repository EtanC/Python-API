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
    data_user = {
        'token': reset['token'], 
    } 
    response = requests.get(f'{config.url}users/all/v1', params=data_user)
    response_data = response.json() 
    del response_data['users'][0]['profile_img_url']
    assert response_data == {'users': [{
        'u_id': reset['auth_user_id'], 
        'email': 'realemail_812@outlook.edu.au', 
        'name_first': 'John', 
        'name_last': 'Smith', 
        'handle_str': 'johnsmith', 
    }]}

def test_two_valid(reset): 
    u_id_1 = reset['auth_user_id']

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

    data_user = { 
        'token': response_data['token'], 
    }
    response = requests.get(f'{config.url}users/all/v1', params=data_user)

    users_list = [{
        'u_id': u_id_1, 
        'email': 'realemail_812@outlook.edu.au', 
        'name_first': 'John', 
        'name_last': 'Smith', 
        'handle_str': 'johnsmith'
    }, 
    {
        'u_id': u_id_2, 
        'email': 'realemail_813@outlook.edu.au', 
        'name_first': 'Tim', 
        'name_last': 'Lee', 
        'handle_str': 'timlee'
    }]
    response_data = response.json() 
    del response_data['users'][0]['profile_img_url']
    del response_data['users'][1]['profile_img_url']
    # sort both lists by u_id to allow direct comparison 
    sorted_users_list = sorted(users_list, key = lambda k: k['u_id']) 
    sorted_response_list = sorted(response_data['users'], key = lambda k: k['u_id']) 

    assert sorted_users_list == sorted_response_list 

def test_three_valid(reset):
    u_id_1 = reset['auth_user_id']

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

    data_register = {
        "email" : "realemail_814@outlook.edu.au",
        "password" : "Password3",
        "name_first" : "Jake",
        "name_last" : "Lee",
    }

    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    data_login = { 
        'email': 'realemail_814@outlook.edu.au', 
        'password': 'Password3', 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)
    response_data = response.json()
    u_id_3 = response_data['auth_user_id']

    data_user = { 
        'token': response_data['token'], 
    }
    response = requests.get(f'{config.url}users/all/v1', params=data_user)

    users_list = [{
        'u_id': u_id_3, 
        'email': 'realemail_814@outlook.edu.au', 
        'name_first': 'Jake', 
        'name_last': 'Lee', 
        'handle_str': 'jakelee'
    },
    {
        'u_id': u_id_1, 
        'email': 'realemail_812@outlook.edu.au', 
        'name_first': 'John', 
        'name_last': 'Smith', 
        'handle_str': 'johnsmith'
    }, 
    {
        'u_id': u_id_2, 
        'email': 'realemail_813@outlook.edu.au', 
        'name_first': 'Tim', 
        'name_last': 'Lee', 
        'handle_str': 'timlee'
    }
    ]

    response_data = response.json() 
    del response_data['users'][0]['profile_img_url']
    del response_data['users'][1]['profile_img_url']
    del response_data['users'][2]['profile_img_url']

    # sort both lists by u_id to allow direct comparison 
    sorted_users_list = sorted(users_list, key = lambda k: k['u_id']) 
    sorted_response_list = sorted(response_data['users'], key = lambda k: k['u_id']) 

    assert sorted_users_list == sorted_response_list 

def test_invalid_user(reset): 
    # token provided is {"name": "Kevin"}
    data_user = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiS2V2aW4ifQ.kEg0Lcmdnk9a5WrUhfSi3F7hRsEHk5-7u7bZ9s49paA',
    }
    response = requests.get(f'{config.url}users/all/v1', params=data_user)

    assert response.status_code == 403 
