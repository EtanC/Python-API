import pytest
from src.error import InputError, AccessError
from fake.other import clear
from fake.auth import auth_register
from fake.channels import channels_create
from fake.channel import channel_join, channel_removeowner, channel_addowner, channel_details

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
def user3():
    return auth_register(
        "realemail_372@outlook.edu.au", "Password2", "Bob", "Bill"
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

@pytest.fixture
def two_owner_channel(channel1, user2):
    channel_join(user2['token'], channel1['channel_id'])
    channel_addowner(
        channel1['user']['token'],
        channel1['channel_id'],
        user2['auth_user_id']
    )
    return {
        'owner1' : channel1['user'],
        'owner2' : user2,
        'channel_id' : channel1['channel_id']
    }

# Test valid remove owner

def test_valid_removeowner(two_owner_channel):
    channel_removeowner(
        two_owner_channel['owner1']['token'],
        two_owner_channel['channel_id'],
        two_owner_channel['owner2']['auth_user_id']
    )
    channel_info = channel_details(
        two_owner_channel['owner1']['token'],
        two_owner_channel['channel_id']
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
    del channel_info['owner_members'][0]['profile_img_url']
    del channel_info['all_members'][0]['profile_img_url']
    del channel_info['all_members'][1]['profile_img_url']
    assert channel_info == expected

def test_global_owner_permissions_removeowner(user1, user2, user3):
    channel_id = channels_create(user2['token'], "Channel1", True)['channel_id']
    # User1 joins channel user2 created, but is not an owner
    channel_join(user1['token'], channel_id)
    # User3 and user2 are owners of the channel
    channel_join(user3['token'], channel_id)
    channel_addowner(user2['token'], channel_id, user3['auth_user_id'])
    # Despite not being owner, user1 should be able to remove user3 from owners
    # Have 2 owners cuz channel must always have 1 owner
    channel_removeowner(user1['token'], channel_id, user3['auth_user_id'])


# Testing invalid remove owner

def test_invalid_token_removeowner(two_owner_channel):
    with pytest.raises(AccessError):
        channel_removeowner(
            'invalid_token',
            two_owner_channel['channel_id'],
            two_owner_channel['owner2']
        )

def test_invalid_channel_id_removeowner(two_owner_channel):
    with pytest.raises(InputError):
        channel_removeowner(
            two_owner_channel['owner1']['token'],
            two_owner_channel['channel_id'] + 1,
            two_owner_channel['owner2']['auth_user_id']
        )

def test_removing_invalid_user_removeowner(two_owner_channel):
    with pytest.raises(InputError):
        channel_removeowner(
            two_owner_channel['owner1']['token'],
            two_owner_channel['channel_id'],
            two_owner_channel['owner2']['auth_user_id'] +
            two_owner_channel['owner1']['auth_user_id'] + 1,
        )

def test_removing_non_owner_removeowner(channel1, user2):
    channel_join(user2['token'], channel1['channel_id'])
    with pytest.raises(InputError):
        channel_removeowner(
            channel1['user']['token'],
            channel1['channel_id'],
            user2['auth_user_id']
        )

def test_remove_only_owner_removeowner(channel1):
    with pytest.raises(InputError):
        channel_removeowner(
            channel1['user']['token'],
            channel1['channel_id'],
            channel1['user']['auth_user_id']
        )

def test_no_owner_permissions_removeowner(two_owner_channel, user3):
    channel_join(user3['token'], two_owner_channel['channel_id'])
    with pytest.raises(AccessError):
        channel_removeowner(
            user3['token'],
            two_owner_channel['channel_id'],
            two_owner_channel['owner1']['auth_user_id']
        )