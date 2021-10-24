import pytest 
import requests
from src import config 

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clear/v1")

# User 1 (global user)
@pytest.fixture
def user1():
    user1_register = {
        'email': "john.smith@gmail.com",
        'password': "password1",
        'name_first': "John",
        'name_last': "Smith",
    }

    response_user1_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user1_register
    )

    auth_user_id = response_user1_register.json()['auth_user_id']
    token        = response_user1_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# User 2 (normal user)
@pytest.fixture
def user2():
    user2_register = {
        'email': "chris.elvin@gmail.com",
        'password': "password2",
        'name_first': "Chris",
        'name_last': "Elvin",
    }

    response_user2_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user2_register
    )

    auth_user_id = response_user2_register.json()['auth_user_id']
    token        = response_user2_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# create private channel called channel2 where user1 will be added
@pytest.fixture
def channel1_private(user1):

    channel1_register = {
        'token': user1['token'],
        'name': "Channel1_Private",
        'is_public': False,
    }

    response_channel1_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel1_register
    )

    channel_id = response_channel1_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

def test_change_to_global_valid(reset_data, user1, user2, channel1_private):
    
    userpermission_change_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id'],
        "permission_id": 1
    }

    requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    join_register = {
        "token": user2['token'],
        "channel_id": channel1_private['channel_id']
    }

    response_join_register = requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    # get the channel1 details to check
    response_join_register = requests.get(
        f"{config.url}channel/details/v2", params=join_register
    )

    response_join_register_data = response_join_register.json()

    owner_members = [
        {
            'u_id': channel1_private['user_id'], 
            'email': "john.smith@gmail.com", 
            'name_first': "John", 
            'name_last': "Smith", 
            'handle_str': "johnsmith",
        }
    ]

    all_members = [
        {
            'u_id': channel1_private['user_id'], 
            'email': "john.smith@gmail.com", 
            'name_first': "John", 
            'name_last': "Smith", 
            'handle_str': "johnsmith",
        },

        {
            'u_id': user2['auth_user_id'], 
            'email': "chris.elvin@gmail.com", 
            'name_first': "Chris", 
            'name_last': "Elvin", 
            'handle_str': "chriselvin",
        }
    ]

    expected_data = {
        "name": "Channel1_Private",
        "is_public": False,
        "owner_members": owner_members,
        "all_members": all_members,
    }

    assert response_join_register_data == expected_data

def test_change_to_member_valid(reset_data, user1, user2, channel1_private):

    # Change user2 to global owner
    userpermission_change_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id'],
        "permission_id": 1
    }

    requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    # Change user2 to back into member
    userpermission_change_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id'],
        "permission_id": 2
    }

    requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    join_register = {
        "token": user2['token'],
        "channel_id": channel1_private['channel_id']
    }

    response_join_register = requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    assert response_join_register.status_code == 403


def test_invalid_u_id(reset_data, user1, user2):

    # Change user2 to global owner
    userpermission_change_register = {
        "token": user1['token'],
        "u_id": user1['auth_user_id'] + user2['auth_user_id'] + 1,
        "permission_id": 1
    }    

    response_userpermission_change = requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    assert response_userpermission_change.status_code == 400


def test_only_global_owner(reset_data, user1):

    # Change user1 to member
    userpermission_change_register = {
        "token": user1['token'],
        "u_id": user1['auth_user_id'],
        "permission_id": 2
    }    

    response_userpermission_change = requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    assert response_userpermission_change.status_code == 400

def test_invalid_permission_id(reset_data, user1, user2):

    # Change user2 to global owner
    userpermission_change_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id'],
        "permission_id": 4
    }    

    response_userpermission_change = requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    assert response_userpermission_change.status_code == 400

def test_not_global_owner(reset_data, user1, user2):

    # Change user2 to global owner
    userpermission_change_register = {
        "token": user2['token'],
        "u_id": user2['auth_user_id'],
        "permission_id": 1
    }    

    response_userpermission_change = requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    assert response_userpermission_change.status_code == 403

def test_invalid_token(reset_data, user1, user2):

    # Change user2 to global owner
    userpermission_change_register = {
        "token": "INVALID_TOKEN",
        "u_id": user2['auth_user_id'],
        "permission_id": 1
    }    

    response_userpermission_change = requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    assert response_userpermission_change.status_code == 403
