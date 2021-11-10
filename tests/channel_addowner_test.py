import pytest
from src.error import InputError, AccessError
from fake.other import clear
from fake.auth import auth_register
from fake.channels import channels_create
from fake.channel import channel_join, channel_addowner, channel_details

@pytest.fixture(autouse=True)
def reset_data():
    clear()

@pytest.fixture
def user1():
    return auth_register(
        "realemail_812@outlook.edu.au", "Password1", "John", "Smith"
    )

@pytest.fixture
def user2():
    return auth_register(
        "realemail_127@outlook.edu.au", "Password1", "Smith", "John"
    )

@pytest.fixture
def channel1(user1):
    channel_id = channels_create(user1['token'], "Channel1", True)['channel_id']
    return {'user' : user1, 'channel_id' : channel_id}

@pytest.fixture
def two_member_channel(channel1, user2):
    channel_join(user2['token'], channel1['channel_id'])
    return {
        'owner' : channel1['user'],
        'member' : user2,
        'channel_id' : channel1['channel_id']
    }


# Test valid addowner
def test_valid_addowner(two_member_channel):
    channel_addowner(
        two_member_channel['owner']['token'],
        two_member_channel['channel_id'],
        two_member_channel['member']['auth_user_id']
    )

    channel_info = channel_details(
        two_member_channel['owner']['token'],
        two_member_channel['channel_id']
    )

    expected = {
        'name': "Channel1",
        'is_public': True,
        'owner_members': [
            {
                'u_id': two_member_channel['owner']['auth_user_id'],
                'email': "realemail_812@outlook.edu.au",
                'name_first': "John",
                'name_last': "Smith",
                'handle_str': "johnsmith",
            },
            {
                'u_id': two_member_channel['member']['auth_user_id'],
                'email': "realemail_127@outlook.edu.au",
                'name_first': "Smith",
                'name_last': "John",
                'handle_str': "smithjohn",
            },
        ],
        'all_members': [
            {
                'u_id': two_member_channel['owner']['auth_user_id'],
                'email': "realemail_812@outlook.edu.au",
                'name_first': "John",
                'name_last': "Smith",
                'handle_str': "johnsmith",
            },
            {
                'u_id': two_member_channel['member']['auth_user_id'],
                'email': "realemail_127@outlook.edu.au",
                'name_first': "Smith",
                'name_last': "John",
                'handle_str': "smithjohn",
            },
        ],
    }
    channel_info['owner_members'].sort(key=lambda x: x['u_id'])
    channel_info['all_members'].sort(key=lambda x: x['u_id'])
    expected['owner_members'].sort(key=lambda x: x['u_id'])
    expected['all_members'].sort(key=lambda x: x['u_id'])

    assert channel_info == expected

# def test_global_owner_addowner():


# Test errors addowner

def test_invalid_channel_id_addowner(two_member_channel):
    with pytest.raises(InputError):
        channel_addowner(
            two_member_channel['owner']['token'],
            two_member_channel['channel_id'] + 1,
            two_member_channel['member']['auth_user_id'],
        )

def test_invalid_u_id_addowner(two_member_channel):
    with pytest.raises(InputError):
        channel_addowner(
            two_member_channel['owner']['token'],
            two_member_channel['channel_id'],
            two_member_channel['member']['auth_user_id'] +
            two_member_channel['owner']['auth_user_id'] + 1
        )

def test_nonmember_addowner(channel1, user2):
    with pytest.raises(InputError):
        channel_addowner(
            channel1['user']['token'],
            channel1['channel_id'],
            user2['auth_user_id']
        )

def test_already_owner_addowner(channel1):
    with pytest.raises(InputError):
        channel_addowner(
            channel1['user']['token'],
            channel1['channel_id'],
            channel1['user']['auth_user_id']
        )

def test_no_owner_permissions_addowner(two_member_channel):
    with pytest.raises(AccessError):
        channel_addowner(
            two_member_channel['member']['token'],
            two_member_channel['channel_id'],
            two_member_channel['member']['auth_user_id']
        )

def test_invalid_token_addowner(two_member_channel):
    with pytest.raises(AccessError):
        channel_addowner(
            "INVALID_TOKEN",
            two_member_channel['channel_id'],
            two_member_channel['member']['auth_user_id']
        )