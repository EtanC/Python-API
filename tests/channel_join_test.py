import pytest 
import requests
from src import config 
# port = 8080
# url = f"http://localhost:{port}/"

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clear/v1")

# create user1
@pytest.fixture
def user1():

    user1_register = {
        'email': "harry.williams@gmail.com",
        'password': "password_harry",
        'name_first': "Harry",
        'name_last': "Williams",
    }

    response_user1_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user1_register
    )

    auth_user_id = response_user1_register.json()['auth_user_id']
    token        = response_user1_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# create puclic channel called channel1 where user1 will be added
@pytest.fixture
def channel1_public(user1):

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

# create private channel called channel2 where user1 will be added
@pytest.fixture
def channel1_private(user1):

    channel2_register = {
        'token': user1['token'],
        'name': "Channel1_Private",
        'is_public': False,
    }

    response_channel2_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel2_register
    )

    channel_id = response_channel2_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

# create user2 which we will use to join channel1
@pytest.fixture
def user2():

    user2_register = {
        'email': "michael.dawson1@gmail.com",
        'password': "michaeldawson",
        'name_first': "Michael",
        'name_last': "Dawson",
    }
    response_user2_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user2_register
    )

    auth_user_id = response_user2_register.json()['auth_user_id']
    token        = response_user2_register.json()['token']
    return {'token' : token, 'auth_user_id' : auth_user_id}

# user2 should be able to join channel1
def test_invalid_token_send(reset_data, user1, channel1_public): 

    token_register_send = {
        "token": "INVALID TOKEN",
        "channel_id": channel1_public['channel_id'],
    }
    
    response_register = requests.post(f"{config.url}channel/join/v1",\
    json=token_register_send)
    assert response_register.status_code == 403

def test_valid_channel_join(reset_data, channel1_public, user2):

    # paramenters for channel/join/v2
    join_register = {
        "token": user2['token'],
        "channel_id": channel1_public['channel_id']
    }

    # allow user2 to join channel1
    requests.post(
        f"{config.url}channel/join/v2", json=join_register
    )

    # get the channel1 details to check
    response_join_register = requests.get(
        f"{config.url}channel/details/v2", params=join_register
    )

    response_join_register_data = response_join_register.json()

    owner_members = [
        {
            'u_id': channel1_public['user_id'], 
            'email': "harry.williams@gmail.com", 
            'name_first': "Harry", 
            'name_last': "Williams", 
            'handle_str': "harrywilliams",
        }
    ]

    all_members = [
        {
            'u_id': channel1_public['user_id'], 
            'email': "harry.williams@gmail.com", 
            'name_first': "Harry", 
            'name_last': "Williams", 
            'handle_str': "harrywilliams",
        },

        {
            'u_id': user2['auth_user_id'], 
            'email': "michael.dawson1@gmail.com", 
            'name_first': "Michael", 
            'name_last': "Dawson", 
            'handle_str': "michaeldawson",
        }
    ]

    expected_data = {
        "name": "Channel1_Public",
        "is_public": True,
        "owner_members": owner_members,
        "all_members": all_members,
    }


    assert response_join_register_data == expected_data

def test_invalid_channel_join(reset_data, channel1_public, user2):

    # paramenters for channel/join/v2
    join_register = {
        "token": user2['token'],
        "channel_id": channel1_public['channel_id'],
    }

    # make an invalid channel ID
    join_register['channel_id'] += 1

    response_join_register = requests.post(f"{config.url}channel/join/v2",\
    json=join_register)
    assert response_join_register.status_code == 400

def test_non_member_private_channel_join(reset_data, channel1_private, user2):

    # paramenters for channel/join/v2
    join_register = {
        "token": user2['token'],
        "channel_id": channel1_private['channel_id'],
    }

    response_join_register = requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    assert response_join_register.status_code == 403
