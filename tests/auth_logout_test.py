import pytest
import requests
from src import config

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clear/v1")

# Test logout

def test_invalid_token_logout(reset_data):
    data_register = {
        'email' : 'realemail_812@outlook.edu.au',
        'password' : 'Password1',
        'name_first' : 'John',
        'name_last' : 'Smith',
    }
    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_logout = {
        'token' : 'Invalid token',
    }
    response_logout = requests.post(
        f"{config.url}auth/logout/v1",
        json=data_logout
    )
    assert response_logout.status_code == 403

# NEED ADMIN REMOVE TO TEST INVALID_USER_ID

def test_invalid_session_id_logout(reset_data):
    data_register = {
        'email' : 'realemail_812@outlook.edu.au',
        'password' : 'Password1',
        'name_first' : 'John',
        'name_last' : 'Smith',
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_logout = {
        'token' : response_register['token'],
    }
    requests.post(
        f"{config.url}auth/logout/v1",
        json=data_logout
    )
    data_logout = {
        'token' : response_register['token'],
    }
    response_logout = requests.post(
        f"{config.url}auth/logout/v1",
        json=data_logout
    )
    assert response_logout.status_code == 403

def test_valid_logout(reset_data):
    data_register = {
        'email' : 'realemail_812@outlook.edu.au',
        'password' : 'Password1',
        'name_first' : 'John',
        'name_last' : 'Smith',
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    data_logout = {
        'token' : response_register['token'],
    }
    requests.post(
        f"{config.url}auth/logout/v1",
        json=data_logout
    )
    data_create = {
        'token' : response_register['token'],
        'name' : 'channel_name',
        'is_public' : True,
    }
    response_create = requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    )
    assert response_create.status_code == 403