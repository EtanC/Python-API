import pytest, requests
from src.standup import standup_start_v1, standup_active_v1
from fake.auth import auth_register
from src.channels import channels_create_v1
from fake.other import clear
from src.error import InputError, AccessError
from src import config

@pytest.fixture(autouse=True)
def reset_data():
    clear()

@pytest.fixture
def user1():

    data_register = {
        'email': "harry.williams@gmail.com",
        'password': "password_harry",
        'name_first': "Harry",
        'name_last': "Williams",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    auth_user_id = response_register.json()['auth_user_id']
    token        = response_register.json()['token']
    return {'token' : token, 'auth_user_id' : auth_user_id}

@pytest.fixture
def user2():
    
    data_register = {
        'email': "michael.dawson1@gmail.com",
        'password': "michaeldawson",
        'name_first': "Michael",
        'name_last': "Dawson",
    }
    response_register = requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )
    auth_user_id = response_register.json()['auth_user_id']
    token = response_register.json()['token']
    return {'token' : token, 'auth_user_id' : auth_user_id}

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
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

# make a 10 sec standup in channel1
@pytest.fixture
def standup1(channel1, user1):

    data_standup = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 2,
    }

    response_standup = requests.post(
        f"{config.url}standup/start/v1",
        json=data_standup
    )

    time_finish = response_standup.json()['time_finish']
    return { 'time_finish' : time_finish }

def test_invalid_token_standup_start(channel1, standup1):

    data_standup = {
        'token' : "INVALID TOKEN",
        'channel_id' : channel1['channel_id']
    }

    response = requests.get(f"{config.url}standup/active/v1", \
        params=data_standup)
    
    assert response.status_code == 403

# Test invalid channel_id
def test_invalid_channel_id_standup_start(channel1, user1):

    data_standup = {
        'token' : user1['token'],
        'channel_id' : channel1['channel_id']
    }
    data_standup['channel_id'] += 1

    response = requests.get(f"{config.url}standup/active/v1", \
        params=data_standup)
    
    assert response.status_code == 400


# Test user not in channel
def test_user_not_in_channel_standup_start(channel1, user2):

    data_standup = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id']
    }


    response = requests.get(f"{config.url}standup/active/v1", \
        params=data_standup)
    
    assert response.status_code == 403


# Test valid standup active check 
def test_valid_standup_active(channel1, standup1, user1):

    time_finish = standup1['time_finish']
    is_active = True
    data_standup = {
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    }
    response_standup = requests.get(f"{config.url}standup/active/v1", \
    params=data_standup)

    response_data = response_standup.json()
    expected_data = {
        'is_active' : is_active,
        'time_finish' : time_finish
    }
    assert expected_data == response_data
