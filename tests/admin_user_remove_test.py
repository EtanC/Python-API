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

# User 3 (normal user)
@pytest.fixture
def user3():
    user3_register = {
        'email': "sam.ross@gmail.com",
        'password': "password3",
        'name_first': "Sam",
        'name_last': "Ross",
    }

    response_user3_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user3_register
    )

    auth_user_id = response_user3_register.json()['auth_user_id']
    token        = response_user3_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# create private channel called channel2 where user1 will be added
@pytest.fixture
def channel1(user1):

    channel1_register = {
        'token': user1['token'],
        'name': "Channel1",
        'is_public': True,
    }

    response_channel1_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel1_register
    )

    channel_id = response_channel1_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

# create private channel called channel2 where user1 will be added
@pytest.fixture
def channel2(user1):

    channel2_register = {
        'token': user1['token'],
        'name': "Channel1",
        'is_public': True,
    }

    response_channel2_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel2_register
    )

    channel_id = response_channel2_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

def test_channel_dm_remove():
    pass


def test_remove_original_owner(reset_data, user1, user2):

    # Change user2 into global owner
    userpermission_change_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id'],
        "permission_id": 2
    }

    requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    user_remove_register = {
        "token": user2['token'],
        "u_id": user1['auth_user_id']
    }

    requests.post(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )



    pass
    


def test_messages_remove(reset_data, user1, user2):
    pass

def test_user_details_remove(reset_data, user1, user2):
    pass

def test_invalid_u_id(reset_data, user1, user2):

    # Change user2 to global owner
    user_remove_register = {
        "token": user1['token'],
        "u_id": user1['auth_user_id'] + user2['auth_user_id'] + 1,
    }    

    response_user_remove = requests.post(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    assert response_user_remove.status_code == 400


def test_only_global_owner(reset_data, user1):

    # Change user1 to member
    user_remove_register = {
        "token": user1['token'],
        "u_id": user1['auth_user_id'],
    }    

    response_user_remove = requests.post(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    assert response_user_remove.status_code == 400

def test_not_global_owner(reset_data, user2):

    # Change user2 to global owner
    user_remove_register = {
        "token": user2['token'],
        "u_id": user2['auth_user_id'],
    }    

    response_user_remove = requests.post(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    assert response_user_remove.status_code == 403