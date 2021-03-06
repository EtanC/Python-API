import pytest
import requests
from src import config

## SETUP

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
def two_member_channel(channel1, user2):
    data_join = {
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
    }
    requests.post(
        f'{config.url}channel/join/v2',
        json=data_join
    )
    return {
        'owner' : channel1['user'],
        'member' : user2,
        'channel_id' : channel1['channel_id']
    }

## TESTS

# Test valid channel_leave

def test_valid_channel_leave(reset_data, two_member_channel):
    data_channel_leave = {
        'token' : two_member_channel['member']['token'],
        'channel_id' : two_member_channel['channel_id'],
    }
    requests.post(
        f'{config.url}channel/leave/v1',
        json=data_channel_leave
    )
    data_details = {
        'token' : two_member_channel['owner']['token'],
        'channel_id' : two_member_channel['channel_id'],
    }
    response_details = requests.get(
        f'{config.url}channel/details/v2',
        params=data_details
    )
    expected = {
        'name' : 'Channel1',
        'is_public' : True,
        'owner_members' : [
            {
                'u_id' : two_member_channel['owner']['auth_user_id'],
                'email' : 'realemail_812@outlook.edu.au',
                'name_first' : 'John',
                'name_last' : 'Smith',
                'handle_str' : 'johnsmith',
            }
        ],
        'all_members' : [
            {
                'u_id' : two_member_channel['owner']['auth_user_id'],
                'email' : 'realemail_812@outlook.edu.au',
                'name_first' : 'John',
                'name_last' : 'Smith',
                'handle_str' : 'johnsmith',
            }
        ]
    }
    details_data = response_details.json() 
    del details_data['owner_members'][0]['profile_img_url']
    del details_data['all_members'][0]['profile_img_url']
    assert details_data == expected

# Need addowner in master

def test_owner_leave_channel_leave(reset_data, two_member_channel):
    data_addowner = {
        'token' : two_member_channel['owner']['token'],
        'channel_id' : two_member_channel['channel_id'],
        'u_id' : two_member_channel['member']['auth_user_id'],
    }
    requests.post(
        f'{config.url}channel/addowner/v1',
        json=data_addowner
    )
    data_channel_leave = {
        'token' : two_member_channel['owner']['token'],
        'channel_id' : two_member_channel['channel_id'],
    }
    requests.post(
        f'{config.url}channel/leave/v1',
        json=data_channel_leave
    )
    data_details = {
        'token' : two_member_channel['member']['token'],
        'channel_id' : two_member_channel['channel_id'],
    }
    response_details = requests.get(
        f'{config.url}channel/details/v2',
        params=data_details
    )
    expected = {
        'name' : 'Channel1',
        'is_public' : True,
        'owner_members' : [
            {
                'u_id' : two_member_channel['member']['auth_user_id'],
                'email': "realemail_127@outlook.edu.au",
                'name_first': "Smith",
                'name_last': "John",
                'handle_str' : 'smithjohn',
            }
        ],
        'all_members' : [
            {
                'u_id' : two_member_channel['member']['auth_user_id'],
                'email': "realemail_127@outlook.edu.au",
                'name_first': "Smith",
                'name_last': "John",
                'handle_str' : 'smithjohn',
            }
        ]
    }
    data_details = response_details.json() 
    del data_details['owner_members'][0]['profile_img_url']
    del data_details['all_members'][0]['profile_img_url']
    assert data_details == expected

def test_only_owner_channel_leave(reset_data, channel1):
    data_channel_leave = {
        'token' : channel1['user']['token'],
        'channel_id' : channel1['channel_id'],
    }
    requests.post(
        f'{config.url}channel/leave/v1',
        json=data_channel_leave
    )
    data_channels_list = {
        'token' : channel1['user']['token'],
        'channel_id' : channel1['channel_id'],
    }
    response_channels_list = requests.get(
        f'{config.url}channels/list/v2',
        params=data_channels_list
    )
    expected = {
        'channels' : [],
    }
    assert response_channels_list.json() == expected

# Test if the messages remain in channel

# Test invalid channel leave

def test_invalid_channel_leave(reset_data, two_member_channel):
    data_channel_leave = {
        'token' : two_member_channel['member']['token'],
        'channel_id' : two_member_channel['channel_id'] + 1,
    }
    response_channel_leave = requests.post(
        f'{config.url}channel/leave/v1',
        json=data_channel_leave
    )
    assert response_channel_leave.status_code == 400

def test_invalid_user_id_channel_leave(reset_data, two_member_channel):
    data_channel_leave = {
        'token' : "INVALID_TOKEN",
        'channel_id' : two_member_channel['channel_id'],
    }
    response_channel_leave = requests.post(
        f'{config.url}channel/leave/v1',
        json=data_channel_leave
    )
    assert response_channel_leave.status_code == 403

def test_non_member_channel_leave(reset_data, channel1, user2):
    data_channel_leave = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
    }
    response_channel_leave = requests.post(
        f'{config.url}channel/leave/v1',
        json=data_channel_leave
    )
    assert response_channel_leave.status_code == 403
