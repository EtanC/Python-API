import pytest
from fake.standup import standup_start, standup_send, standup_active
from fake.auth import auth_register
from fake.channels import channels_create
from fake.other import clear
from src.error import InputError, AccessError
import time

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

# make a 10 sec standup in channel1
@pytest.fixture
def standup1(channel1):
    time_finish = standup_start(channel1['user']['token'], channel1['channel_id'], 10)['time_finish']
    return {'time_finish': time_finish}

# Test invalid token
def test_invalid_token_standup_start(channel1):
    with pytest.raises(AccessError):
        standup_active("Invalid token", channel1['channel_id'])

# Test invalid channel_id
def test_invalid_channel_id_standup_start(channel1):
    with pytest.raises(InputError):
        standup_active(channel1['user']['token'], channel1['channel_id'] + 1)
   
# Test user not in channel
def test_user_not_in_channel_standup_start(channel1, user2):
    with pytest.raises(AccessError):
        standup_active(user2['token'], channel1['channel_id'])

# Test valid standup active check - still active
def test_valid_standup_active_ACTIVE(channel1, standup1):
    time_finish = standup1['time_finish']
    is_active = True

    data_standup = {
        'token': channel1['user']['token'],
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
