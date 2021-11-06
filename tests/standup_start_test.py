import pytest
from fake.standup import standup_start, standup_send, standup_active
from fake.auth import auth_register
from fake.channels import channels_create
from fake.other import clear
from src.error import InputError, AccessError

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
    channel_id = channels_create(user1['token'], "channel1", True)['channel_id']
    return {'user' : user1, 'channel_id' : channel_id}

# Test valid standup
    # All messages from standup packaged as single message from standup starter
def test_valid_standup_start(channel1):
    standup_start(channel1['user']['token'], channel1['channel_id'], 2)
    assert standup_active(
        channel1['user']['token'],
        channel1['channel_id']
    )['is_active']

# Test invalid token
def test_invalid_token_standup_start(channel1):
    with pytest.raises(AccessError):
        standup_start("Invalid token", channel1['channel_id'], 2)

# Test invalid channel_id
def test_invalid_channel_id_standup_start(channel1):
    with pytest.raises(InputError):
        standup_start(channel1['user']['token'], channel1['channel_id'] + 1, 2)

# Test negative length
def test_negative_length_standup_start(channel1):
    with pytest.raises(InputError):
        standup_start(channel1['user']['token'], channel1['channel_id'], -2)

# Test standup already active
def test_standup_already_active_standup_start(channel1):
    standup_start(channel1['user']['token'], channel1['channel_id'], 2)
    with pytest.raises(InputError):
        standup_start(channel1['user']['token'], channel1['channel_id'], 2)

# Test user not in channel
def test_user_not_in_channel_standup_start(channel1, user2):
    with pytest.raises(AccessError):
        standup_start(user2['token'], channel1['channel_id'], 2)