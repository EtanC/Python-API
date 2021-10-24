import pytest
import requests
from src import config

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clear/v1")

@pytest.fixture
def user1():
    data_register = {
        'email': "realemail_812@outlook.edu.au",
        'password': "Password1",
        'name_first': "John",
        'name_last': "Smith",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    return response_register.json()

@pytest.fixture
def user2():
    data_register2 = {
        'email': "realemail_127@outlook.edu.au",
        'password': "Password1",
        'name_first': "Smith",
        'name_last': "John",
    }
    response_register2 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register2
    )
    return response_register2.json()

@pytest.fixture
def user3():
    data_register2 = {
        'email': "realemail_372@outlook.edu.au",
        'password': "Password2",
        'name_first': "Bob",
        'name_last': "Bill",
    }
    response_register2 = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register2
    )
    return response_register2.json()

@pytest.fixture
def channel1(user1):
    data_create = {
        'token': user1['token'],
        'name': "Channel1",
        'is_public': True,
    }
    response_create = requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    )
    channel_id = response_create.json()['channel_id']
    return {'user' : user1, 'channel_id' : channel_id}


@pytest.fixture
def two_owner_channel(channel1, user2):
    data_join = {
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
    }
    requests.post(
        f"{config.url}channel/join/v2",
        json=data_join
    )
    data_addowner = {
        'token': channel1['user']['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user2['auth_user_id'],
    }
    requests.post(
        f"{config.url}channel/addowner/v1",
        json=data_addowner
    )
    return {
        'owner1' : channel1['user'],
        'owner2' : user2,
        'channel_id' : channel1['channel_id']
    }

# Test valid remove owner

def test_valid_removeowner(reset_data, two_owner_channel):
    data_removeowner = {
        'token': two_owner_channel['owner1']['token'],
        'channel_id': two_owner_channel['channel_id'],
        'u_id': two_owner_channel['owner2']['auth_user_id'],
    }
    requests.post(
        f"{config.url}channel/removeowner/v1",
        json=data_removeowner
    )
    data_details = {
        'token': two_owner_channel['owner1']['token'],
        'channel_id': two_owner_channel['channel_id'],
    }
    response_details = requests.get(
        f"{config.url}channel/details/v2",
        params=data_details
    )
    expected = {
        'name': "Channel1",
        'is_public': True,
        'owner_members': [
            {
                'u_id': two_owner_channel['owner1']['auth_user_id'],
                'email': "realemail_812@outlook.edu.au",
                'name_first': "John",
                'name_last': "Smith",
                'handle_str': "johnsmith",
            },
        ],
        'all_members': [
            {
                'u_id': two_owner_channel['owner1']['auth_user_id'],
                'email': "realemail_812@outlook.edu.au",
                'name_first': "John",
                'name_last': "Smith",
                'handle_str': "johnsmith",
            },
            {
                'u_id': two_owner_channel['owner2']['auth_user_id'],
                'email': "realemail_127@outlook.edu.au",
                'name_first': "Smith",
                'name_last': "John",
                'handle_str': "smithjohn",
            },
        ],
    }
    assert response_details.json() == expected

# Testing invalid remove owner

def test_invalid_token_removeowner(reset_data, two_owner_channel):
    data_removeowner = {
        'token': 'invalid_token',
        'channel_id': two_owner_channel['channel_id'],
        'u_id': two_owner_channel['owner2'],
    }
    response_removeowner = requests.post(
        f"{config.url}channel/removeowner/v1",
        json=data_removeowner
    )
    assert response_removeowner.status_code == 403

def test_invalid_channel_id_removeowner(reset_data, two_owner_channel):
    data_removeowner = {
        'token': two_owner_channel['owner1']['token'],
        'channel_id': two_owner_channel['channel_id'] + 1,
        'u_id': two_owner_channel['owner2']['auth_user_id'],
    }
    response_removeowner = requests.post(
        f"{config.url}channel/removeowner/v1",
        json=data_removeowner
    )
    assert response_removeowner.status_code == 400

def test_removing_invalid_user_removeowner(reset_data, two_owner_channel):
    data_removeowner = {
        'token': two_owner_channel['owner1']['token'],
        'channel_id': two_owner_channel['channel_id'],
        'u_id': two_owner_channel['owner2']['auth_user_id']
                + two_owner_channel['owner1']['auth_user_id'] + 1,
    }
    response_removeowner = requests.post(
        f"{config.url}channel/removeowner/v1",
        json=data_removeowner
    )
    assert response_removeowner.status_code == 400

def test_removing_non_owner_removeowner(reset_data, channel1, user2):
    data_join = {
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
    }
    requests.post(
        f"{config.url}channel/join/v2",
        json=data_join
    )
    data_removeowner = {
        'token': channel1['user']['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user2['auth_user_id'],
    }
    response_removeowner = requests.post(
        f"{config.url}channel/removeowner/v1",
        json=data_removeowner
    )
    assert response_removeowner.status_code == 400

def test_remove_only_owner_removeowner(reset_data, channel1):
    data_removeowner = {
        'token': channel1['user']['token'],
        'channel_id': channel1['channel_id'],
        'u_id': channel1['user']['auth_user_id'],
    }
    response_removeowner = requests.post(
        f"{config.url}channel/removeowner/v1",
        json=data_removeowner
    )
    assert response_removeowner.status_code == 400

def test_no_owner_permissions_removeowner(reset_data, two_owner_channel, user3):
    data_join = {
        'token': user3['token'],
        'channel_id': two_owner_channel['channel_id'],
    }
    requests.post(
        f"{config.url}channel/join/v2",
        json=data_join
    )
    data_removeowner = {
        'token': user3['token'],
        'channel_id': two_owner_channel['channel_id'],
        'u_id': two_owner_channel['owner1']['auth_user_id'],
    }
    response_removeowner = requests.post(
        f"{config.url}channel/removeowner/v1",
        json=data_removeowner
    )
    assert response_removeowner.status_code == 403