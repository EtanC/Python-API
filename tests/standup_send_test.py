import pytest
from fake.standup import standup_start, standup_send
from fake.auth import auth_register
from fake.channels import channels_create
from fake.channel import channel_messages
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

def test_standup_send_valid(channel1): 
    # activate stand up
    standup_start(channel1['user']['token'], channel1['channel_id'], 3)
    # send message 
    message = 'Hello from the other side'
    standup_send(channel1['user']['token'], channel1['channel_id'], message)
    time.sleep(5)
    channel_message = channel_messages(channel1['user']['token'], channel1['channel_id'], 0)
    print(channel_message)
    del channel_message['messages'][0]['time_created']
    del channel_message['messages'][0]['reacts']
    del channel_message['messages'][0]['is_pinned']
    assert channel_message == {
        'messages': [{
            'message_id': 1, 
            'u_id': channel1['user']['auth_user_id'], 
            'message': message, 
            }], 
        'start': 0,
        'end': -1
    }

# ACCESS ERROR ######
# Invalid token
def test_invalid_token_standup_send(channel1):
    message = 'Hello from the other side'
    with pytest.raises(AccessError):
        standup_send("Invalid token", channel1['channel_id'], message)


# Test user not in channel
def test_user_not_in_channel_standup_start(channel1, user2):
    message = 'Hello from the other side'
    with pytest.raises(AccessError):
        standup_send(user2['token'], channel1['channel_id'], message)

# INPUT ERROR #####
# Test invalid channel_id
def test_invalid_channel_id_standup_send(channel1):
    message = 'Hello from the other side'
    with pytest.raises(InputError):
        standup_send(channel1['user']['token'], channel1['channel_id'] + 1, message)

# Test when there is no stand up in the channel
def test_standup_already_active_standup_start(channel1):
    message = 'Hello from the other side'
    with pytest.raises(InputError):
        standup_send(channel1['user']['token'], channel1['channel_id'], message)

# Test for message over 1000 characters
def test_long_message_standup_send(channel1): 
    message = 'No' * 1200
    with pytest.raises(InputError):
        standup_send(channel1['user']['token'], channel1['channel_id'], message)