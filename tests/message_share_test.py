import pytest 
import requests
from src import config 
from datetime import datetime, timezone

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
        'email': "johnny.jacobs@gmail.com",
        'password': "password3",
        'name_first': "Johnny",
        'name_last': "Jacobs",
    }

    response_user3_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user3_register
    )

    auth_user_id = response_user3_register.json()['auth_user_id']
    token        = response_user3_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# create public channel called channel1 where user1 will be added
@pytest.fixture
def channel1(user1):

    channel1_register = {
        'token': user1['token'],
        'name': "Channel1_Public",
        'is_public': True,
    }

    response_channel1_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel1_register
    )

    channel_id = response_channel1_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

# create public channel called channel2 where user1 will be added
@pytest.fixture
def channel2(user1):

    channel2_register = {
        'token': user1['token'],
        'name': "Channel2_Public",
        'is_public': True,
    }

    response_channel2_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel2_register
    )

    channel_id = response_channel2_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

# create dm1 with user1 and user2
@pytest.fixture
def dm1(user1, user2):

    u_ids = []
    u_ids.append(user2['auth_user_id'])

    #user1 creates a dm with user2 included
    data_create = {
        'token': user1['token'],
        'u_ids': u_ids
    }

    response_create = requests.post(
        f"{config.url}dm/create/v1",
        json=data_create
    )
    dm_id   = response_create.json()['dm_id']
    owner   = user1

    return {'dm_id' : dm_id, 'owner': owner, 'all_users': u_ids}

# create dm2 with user1 and user3
@pytest.fixture
def dm2(user1, user3):

    u_ids = []
    u_ids.append(user3['auth_user_id'])

    #user1 creates a dm with user2 included
    data_create = {
        'token': user1['token'],
        'u_ids': u_ids
    }

    response_create = requests.post(
        f"{config.url}dm/create/v1",
        json=data_create
    )
    dm_id   = response_create.json()['dm_id']
    owner   = user1

    return {'dm_id' : dm_id, 'owner': owner, 'all_users': u_ids}

# Send a message to channel1 which will be shared
@pytest.fixture
def message_to_share_channel(channel1, user1):

    message = "To_BE_SHARED!!"

    data_send = {
        'token' : user1['token'],
        'channel_id' : channel1['channel_id'],
        'message' : message
    }

    response_send = requests.post(
        f"{config.url}message/send/v1",
        json=data_send
    )

    message_id = response_send.json()['message_id']
    return {'message_id' : message_id, 'message': message}

@pytest.fixture
def message_to_share_dm(dm1, user1):

    message = "To_BE_SHARED_DM!!"

    data_send = {
        'token' : user1['token'],
        'dm_id' : dm1['dm_id'],
        'message' : message
    }

    response_send = requests.post(
        f"{config.url}message/senddm/v1",
        json=data_send
    )

    message_id = response_send.json()['message_id']
    return {'message_id' : message_id, 'message': message}


# share a message from channel1 to channel2
def test_valid_share_channel(user1, channel2, message_to_share_channel):

    data_share = {
        'token' : user1['token'],
        'og_message_id' : message_to_share_channel['message_id'],
        'message' : "XDDD", 
        'channel_id' : channel2['channel_id'], 
        'dm_id' : -1
    }

    response_share = requests.post(
        f"{config.url}message/share/v1",
        json=data_share
    )

    response_data = response_share.json()
    expected_data = {
        'shared_message_id' : 1
    }

    assert response_data == expected_data

# share a message from channel1 to channel2
def test_valid_share_dm(user1, dm2, message_to_share_dm):

    data_share = {
        'token' : user1['token'],
        'og_message_id' : message_to_share_dm['message_id'],
        'message' : "XDDD", 
        'channel_id' : -1, 
        'dm_id' : dm2['dm_id']
    }

    response_share = requests.post(
        f"{config.url}message/share/v1",
        json=data_share
    )

    response_data = response_share.json()
    expected_data = {
        'shared_message_id' : 1
    }

    assert response_data == expected_data

def test_invalid_channel_and_dm(user1, channel2, message_to_share_channel):
    #400
    data_share = {
        'token' : user1['token'],
        'og_message_id' : message_to_share_channel['message_id'],
        'message' : "XDDD", 
        'channel_id' : channel2['channel_id'], 
        'dm_id' : -1
    }

    data_share['channel_id'] += 1
    data_share['dm_id'] += 1

    response_share = requests.post(
        f"{config.url}message/share/v1",
        json=data_share
    )
    
    assert response_share.status_code == 400

def test_no_negative_one():
    #400
    pass

def test_invalid_message():
    #400
    pass

def test_message_too_long():
    #400
    pass

def test_user_not_in_channel():
    #403
    pass

def test_invalid_token():
    #403
    pass