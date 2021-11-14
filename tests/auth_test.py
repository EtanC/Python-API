import pytest
import requests
from src import config

# Black box test valid register and login (testing auth.py)

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clear/v1")

# Testing token

def test_valid_register(reset_data):
    data_register = {
        "email" : "realemail_812@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "John",
        "name_last" : "Smith",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_create = {
        'token' : response_register.json()['token'],
        'name' : "channel",
        'is_public' : True,
    }
    response_create = requests.post(
        f"{config.url}channels/create/v2",
        json=data_create,
    )
    assert response_create.status_code == 200

# ADD TEST WITH LOGOUT

def test_valid_two_sessions_register(reset_data):
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
        "email" : "realemail_812@outlook.edu.au",
        "password" : "Password1",
    }
    response_login = requests.post(
        f"{config.url}auth/login/v2",
        json=data_login
    )
    data_create = {
        'token' : response_login.json()['token'],
        'name' : "channel",
        'is_public' : True,
    }
    response_create = requests.post(
        f"{config.url}channels/create/v2",
        json=data_create,
    )
    assert response_create.status_code == 200

# Testing handle_str

def test_handle_str(reset_data):
    data_register = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
        "name_first": "John",
        "name_last": "Smith",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    token = response_register.json()['token']
    data_create = {
        'token': token,
        'name': "channel_name",
        'is_public': True,
    }
    response_create = requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    )
    channel_id = response_create.json()['channel_id']
    data_details = {
        'token': token,
        'channel_id': channel_id,
    }
    response_details = requests.get(
        f"{config.url}channel/details/v2",
        params=data_details
    )
    u_id = response_register.json()['auth_user_id']
    expected = {
        'name' : "channel_name",
        'is_public' : True,
        'owner_members' : [
            {
                'u_id' : u_id,
                'email' : "realemail_812@outlook.edu.au",
                'name_first' : "John",
                'name_last' : "Smith",
                'handle_str' : "johnsmith",
            },
        ],
        'all_members' : [
            {
                'u_id' : u_id,
                'email' : "realemail_812@outlook.edu.au",
                'name_first' : "John",
                'name_last' : "Smith",
                'handle_str' : "johnsmith",
            },
        ],
    }
    details_data = response_details.json()
    del details_data['owner_members'][0]['profile_img_url']
    del details_data['all_members'][0]['profile_img_url']
    
    assert details_data == expected

def test_handle_str_repeated(reset_data):
    data_register = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
        "name_first": "John",
        "name_last": "Smith",
    }
    requests.post(f"{config.url}auth/register/v2", json=data_register)
    data_register2 = {
        "email": "realemail_289@outlook.edu.au",
        "password": "Password1",
        "name_first": "John",
        "name_last": "Smith",
    }
    response_register2 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register2
    )
    token2 = response_register2.json()['token']
    data_create = {
        'token': token2,
        'name': "channel_name",
        'is_public': True,
    }
    response_create = requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    )
    channel_id = response_create.json()['channel_id']
    data_details = {
        'token': token2,
        'channel_id': channel_id,
    }
    response_details = requests.get(
        f"{config.url}channel/details/v2",
        params=data_details
    )
    u_id2 = response_register2.json()['auth_user_id']
    expected = {
        'name' : "channel_name",
        'is_public' : True,
        'owner_members' : [
            {
                'u_id' : u_id2,
                'email' : "realemail_289@outlook.edu.au",
                'name_first' : "John",
                'name_last' : "Smith",
                'handle_str' : "johnsmith0",
            },
        ],
        'all_members' : [
            {
                'u_id' : u_id2,
                'email' : "realemail_289@outlook.edu.au",
                'name_first' : "John",
                'name_last' : "Smith",
                'handle_str' : "johnsmith0",
            },
        ],
    }
    details_data = response_details.json() 
    del details_data['owner_members'][0]['profile_img_url']
    del details_data['all_members'][0]['profile_img_url']
    assert details_data == expected

# Tests for error checking auth_register

def test_invalid_email_register(reset_data):
    data_register = {
        "email": "uhh, im also a real email?",
        "password": "asdfghjkl",
        "name_first": "Bill",
        "name_last": "Thompson",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    assert response_register.status_code == 400

def test_email_repeat_register(reset_data):
    data_register = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
        "name_first": "John",
        "name_last": "Smith",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    assert response_register.status_code == 200
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    assert response_register.status_code == 400

def test_short_password_register(reset_data):
    data_register = {
        "email": "realemail_812@outlook.edu.au",
        "password": "short",
        "name_first": "John",
        "name_last": "Smith",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    assert response_register.status_code == 400

def test_long_firstname_register(reset_data):
    data_register = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
        "name_first": "John" * 20,
        "name_last": "Smith",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    assert response_register.status_code == 400

def test_long_lastname_register(reset_data):
    data_register = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
        "name_first": "John",
        "name_last": "Smith" * 20,
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    assert response_register.status_code == 400

# Test for error checking auth_login

def test_wrong_password_login(reset_data):
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
        "email" : "realemail_812@outlook.edu.au",
        "password": "wrong_password",
    }
    response_login = requests.post(
        f"{config.url}auth/login/v2",
        json=data_login
    )
    assert response_login.status_code == 400

def test_wrong_email_login(reset_data):
    data_register = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
        "name_first": "John",
        "name_last": "Smith",
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_login = {
        "email": "wrong_email@outlook.com",
        "password": "Password1",
    }
    response_login = requests.post(
        f"{config.url}auth/login/v2",
        json=data_login
    )
    assert response_login.status_code == 400