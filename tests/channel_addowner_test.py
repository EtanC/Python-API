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
    return response_register.json()['auth_user_id']

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
    return response_register2.json()['auth_user_id']

@pytest.fixture
def channel1(user1):
    data_create = {
        'auth_user_id': user1,
        'name': "Channel1",
        'is_public': True,
    }
    response_create = requests.post(
        f"{config.url}channels/create/v2",
        json=data_create
    )
    channel_id = response_create.json()['channel_id']
    return {'user_id' : user1, 'channel_id' : channel_id}

@pytest.fixture
def two_member_channel(channel1, user2):
    data_join = {
        'auth_user_id': user2,
        'channel_id': channel1['channel_id'],
    }
    requests.post(
        f"{config.url}channel/join/v2",
        json=data_join
    )
    return {
        'owner' : channel1['user_id'],
        'member' : user2,
        'channel_id' : channel1['channel_id']
    }


# Test valid addowner
def test_valid_addowner(reset_data, two_member_channel):
    data_addowner = {
        'auth_user_id': two_member_channel['owner'],
        'channel_id': two_member_channel['channel_id'],
        'u_id': two_member_channel['member'],
    }
    requests.post(
        f"{config.url}channel/addowner/v1",
        json=data_addowner
    )
    data_details = {
        'auth_user_id': two_member_channel['owner'],
        'channel_id': two_member_channel['channel_id'],
    }
    response_details = requests.get(
        f"{config.url}channel/details/v2",
        json=data_details
    )

    expected = {
        'name': "Channel1",
        'is_public': True,
        'owner_members': [
            {
                'u_id': two_member_channel['owner'],
                'email': "realemail_812@outlook.edu.au",
                'name_first': "John",
                'name_last': "Smith",
                'handle_str': "johnsmith",
            },
            {
                'u_id': two_member_channel['member'],
                'email': "realemail_127@outlook.edu.au",
                'name_first': "Smith",
                'name_last': "John",
                'handle_str': "smithjohn",
            },
        ],
        'all_members': [
            {
                'u_id': two_member_channel['owner'],
                'email': "realemail_812@outlook.edu.au",
                'name_first': "John",
                'name_last': "Smith",
                'handle_str': "johnsmith",
            },
            {
                'u_id': two_member_channel['member'],
                'email': "realemail_127@outlook.edu.au",
                'name_first': "Smith",
                'name_last': "John",
                'handle_str': "smithjohn",
            },
        ],
    }
    assert response_details.json() == expected

# Test errors addowner

def test_invalid_channel_id_addowner(reset_data, two_member_channel):
    data_addowner = {
        'auth_user_id': two_member_channel['owner'],
        'channel_id': two_member_channel['channel_id'] + 1,
        'u_id': two_member_channel['member'],
    }
    response_addowner = requests.post(
        f"{config.url}channel/addowner/v1",
        json=data_addowner
    )
    assert response_addowner.status_code == 400

def test_invalid_u_id_addowner(reset_data, two_member_channel):
    data_addowner = {
        'auth_user_id': two_member_channel['owner'],
        'channel_id': two_member_channel['channel_id'],
        'u_id': two_member_channel['member'] + two_member_channel['owner'] + 1,
    }
    response_addowner = requests.post(
        f"{config.url}channel/addowner/v1",
        json=data_addowner
    )
    assert response_addowner.status_code == 400

def test_nonmember_addowner(reset_data, channel1, user2):
    data_addowner = {
        'auth_user_id': channel1['user_id'],
        'channel_id': channel1['channel_id'],
        'u_id': user2,
    }
    response_addowner = requests.post(
        f"{config.url}channel/addowner/v1",
        json=data_addowner
    )
    assert response_addowner.status_code == 400

def test_already_owner_addowner(reset_data, channel1):
    data_addowner = {
        'auth_user_id': channel1['user_id'],
        'channel_id': channel1['channel_id'],
        'u_id': channel1['user_id'],
    }
    response_addowner = requests.post(
        f"{config.url}channel/addowner/v1",
        json=data_addowner
    )
    assert response_addowner.status_code == 400

def test_no_owner_permissions_addowner(reset_data, two_member_channel):
    data_addowner = {
        'auth_user_id': two_member_channel['member'],
        'channel_id': two_member_channel['channel_id'],
        'u_id': two_member_channel['member'],
    }
    response_addowner = requests.post(
        f"{config.url}channel/addowner/v1",
        json=data_addowner
    )
    assert response_addowner.status_code == 403

def test_invalid_user_id_addowner(reset_data, two_member_channel):
    data_addowner = {
        'auth_user_id': two_member_channel['owner'] + 
                        two_member_channel['member'] + 1,
        'channel_id': two_member_channel['channel_id'],
        'u_id': two_member_channel['member'],
    }
    response_addowner = requests.post(
        f"{config.url}channel/addowner/v1",
        json=data_addowner
    )
    assert response_addowner.status_code == 403