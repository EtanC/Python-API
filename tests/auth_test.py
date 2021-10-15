import pytest
import requests
from src import config

# Black box test valid register and login (testing auth.py)

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clear/v1")

def test_valid(reset_data):
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
    data_login = {
        "email" : "realemail_812@outlook.edu.au",
        "password" : "Password1",
    }
    response_login = requests.post(
        f"{config.url}auth/login/v2",
        json=data_login
    )
    assert response_login.json() == response_register.json()

# Testing handle_str

## MUST IMPLEMENT DETAILS ROUTE FIRST

# def test_handle_str(reset_data):
#     data_register = {
#         "email": "realemail_812@outlook.edu.au",
#         "password": "Password1",
#         "name_first": "John",
#         "name_last": "Smith",
#     }
#     response_register = requests.post(
#         f"{config.url}auth/register/v2",
#         json=data_register
#     )
#     user_id = response_register.json()['auth_user_id']
#     data_create = {
#         'auth_user_id': user_id,
#         'name': "channel_name",
#         'is_public': True,
#     }
#     response_create = requests.post(
#         f"{config.url}channels/create/v2",
#         json=data_create
#     )
#     channel_id = response_create.json()['channel_id']
#     data_details = {
#         'auth_user_id': user_id,
#         'channel_id': channel_id,
#     }
#     response_details = requests.post(
#         f"{config.url}channel/details/v2",
#         json=data_details
#     )
#     expected = {
#         'name' : "channel_name",
#         'is_public' : True,
#         'owner_members' : [
#             {
#                 'email' : "realemail_812@outlook.edu.au",
#                 'name_first' : "John",
#                 'name_last' : "Smith",
#                 'handle_str' : "johnsmith",
#             },
#         ],
#         'all_members' : [
#             {
#                 'email' : "realemail_812@outlook.edu.au",
#                 'name_first' : "John",
#                 'name_last' : "Smith",
#                 'handle_str' : "johnsmith",
#             },
#         ],
#     }
#     assert response_details.json() == expected

# def test_handle_str_repeated(reset_data):
#     data_register = {
#         "email": "realemail_812@outlook.edu.au",
#         "password": "Password1",
#         "name_first": "John",
#         "name_last": "Smith",
#     }
#     requests.post(f"{config.url}auth/register/v2", json=data_register)
#     data_register2 = {
#         "email": "realemail_289@outlook.edu.au",
#         "password": "Password1",
#         "name_first": "John",
#         "name_last": "Smith",
#     }
#     response_register2 = requests.post(
#         f"{config.url}auth/register/v2",
#         json=data_register2
#     )
#     user_id2 = response_register2.json()['auth_user_id']
#     data_create = {
#         'auth_user_id': user_id2,
#         'name': "channel_name",
#         'is_public': True,
#     }
#     response_create = requests.post(
#         f"{config.url}channels/create/v2",
#         json=data_create
#     )
#     channel_id = response_create.json()['channel_id']
#     data_details = {
#         'auth_user_id': user_id2,
#         'channel_id': channel_id,
#     }
#     response_details = requests.post(
#         f"{config.url}channel/details/v2",
#         json=data_details
#     )
#     expected = {
#         'name' : "channel_name",
#         'is_public' : True,
#         'owner_members' : [
#             {
#                 'email' : "realemail_289@outlook.edu.au",
#                 'name_first' : "John",
#                 'name_last' : "Smith",
#                 'handle_str' : "johnsmith0",
#             },
#         ],
#         'all_members' : [
#             {
#                 'email' : "realemail_289@outlook.edu.au",
#                 'name_first' : "John",
#                 'name_last' : "Smith",
#                 'handle_str' : "johnsmith0",
#             },
#         ],
#     }
#     assert response_details.json() == expected

# Tests for error checking auth_register

def test_invalid_email(reset_data):
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

def test_email_repeat(reset_data):
    data_register = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
        "name_first": "John",
        "name_last": "Smith",
    }
    data_login = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    response_login = requests.post(
        f"{config.url}auth/login/v2",
        json=data_login
    )
    assert response_login.json() == response_register.json()
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    assert response_register.status_code == 400

def test_short_password(reset_data):
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

def test_long_firstname(reset_data):
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

def test_long_lastname(reset_data):
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

def test_wrong_password(reset_data):
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
    
    data_login = {
        "email" : "realemail_812@outlook.edu.au",
        "password": "wrong_password",
    }
    response_login = requests.post(
        f"{config.url}auth/login/v2",
        json=data_login
    )
    assert response_login.status_code == 400

def test_wrong_email(reset_data):
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
    data_login = {
        "email": "wrong_email@outlook.com",
        "password": "Password1",
    }
    response_login = requests.post(
        f"{config.url}auth/login/v2",
        json=data_login
    )
    assert response_login.status_code == 400