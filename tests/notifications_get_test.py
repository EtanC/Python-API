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

# create public channel called channel2 where user1 will be added
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

# Only using tagged for this test
def test_valid_notification(reset_data, user1, user2, channel1):

    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith hi',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    notifications_register = {
        "token": user1['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = [{
        "channel_id": channel1['channel_id'],
        "dm_id": -1,
        "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith hi'
    }]

    assert data_notifications_get == expected_data

# Only using tagged for this test
def test_many_notifications(reset_data, user1, user2, channel1):
    
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith hi',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith Whats up?',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith Watch it!',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    notifications_register = {
        "token": user1['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = [
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith Watch it!'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith Whats up?'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith hi'
        }
    ]

    assert data_notifications_get == expected_data

# Only using tagged for this test
def test_limit_notifications(reset_data, user1, user2, channel1):
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    # Message 1
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith hi',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 2
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith Whats up?',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 3
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith Watch it!',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 4
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith hello',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 5
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith u there?',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 6
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith helloooo',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 7
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith where r u',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 8
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith hellooo',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 9
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith spam',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 10
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith spam',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 11
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith respond?',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 12
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith u hate me',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 13
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith hello?',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 14
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith im crying',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 15
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith TT',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 16
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith whyyyy',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 17
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith pleaseee',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 18
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith i beg u',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 19
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith u busy?',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 20
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith im done',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    # Message 21
    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith bye',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    notifications_register = {
        "token": user1['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = [
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith bye'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith im done'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith u busy?'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith i beg u'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith pleaseee'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith whyyyy'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith TT'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith im crying'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith hello?'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith u hate me'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith respond?'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith spam'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith spam'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith hellooo'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith where r u'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith helloooo'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith u there?'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith hello'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith Watch it!'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith Whats up?'
        }
    ]

    assert data_notifications_get == expected_data

# Testing reacts
def test_react_notification(reset_data, user1, user2, channel1):
    
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(f"{config.url}channel/join/v2",\
    json=join_register)
    
    message_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id'],
        "message": 'hello'
    }
    message = requests.post(
        f"{config.url}message/send/v1",
        json=message_register
    )

    message_id = message.json()['message_id']

    react_register = {
        "token": user1['token'],
        "message_id": message_id,
        "react_id": 1
    }
    requests.post(
        f"{config.url}message/react/v1",
        json=react_register
    )

    notifications_register = {
        "token": user2['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = [{
        "channel_id": channel1['channel_id'],
        "dm_id": -1,
        "notification_message": 'johnsmith reacted to your message in Channel1_Public'
    }]

    assert data_notifications_get == expected_data

# Test for getting added to a channel
def test_added_to_channel(reset_data, user1, user2, channel1):
    
    # input parameters for channel_invite_v2
    invite_register = {
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    }

    # invite user2 to the channel
    requests.post(
        f"{config.url}channel/invite/v2", json=invite_register
    )

    notifications_register = {
        "token": user2['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = [{
        "channel_id": channel1['channel_id'],
        "dm_id": -1,
        "notification_message": 'johnsmith added you to Channel1_Public'
    }]

    assert data_notifications_get == expected_data

# Test for getting added to a dm
def test_added_to_dm(reset_data, user1, user2, channel1):
    
    data = {
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id = response.json()['dm_id']

    notifications_register = {
        "token": user2['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = [{
        "channel_id": -1,
        "dm_id": dm_id,
        "notification_message": 'johnsmith added you to chriselvin, johnsmith'
    }]

    assert data_notifications_get == expected_data

# Test for when the message is greater than 20 characters
def test_long_message(reset_data, user1, user2, channel1):
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@johnsmith How are you today?',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    notifications_register = {
        "token": user1['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = [{
        "channel_id": channel1['channel_id'],
        "dm_id": -1,
        "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith How are y'
    }]

    assert data_notifications_get == expected_data

# Testing a mix of tagged, reacts and adds for timestamps
def test_mixed_notifications(reset_data, user1, user2, channel1):
    # input parameters for channel_invite_v2
    invite_register = {
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    }

    # invite user2 to the channel
    requests.post(
        f"{config.url}channel/invite/v2", json=invite_register
    )

    message_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id'],
        "message": 'hello'
    }
    message = requests.post(
        f"{config.url}message/send/v1",
        json=message_register
    )

    message_id = message.json()['message_id']

    react_register = {
        "token": user1['token'],
        "message_id": message_id,
        "react_id": 1
    }
    requests.post(
        f"{config.url}message/react/v1",
        json=react_register
    )

    data_send_message = {
        'token' : user1['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@chriselvin hello!',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    notifications_register = {
        "token": user2['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = [
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'johnsmith tagged you in Channel1_Public: @chriselvin hello!'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'johnsmith reacted to your message in Channel1_Public'
        },
        {
            "channel_id": channel1['channel_id'],
            "dm_id": -1,
            "notification_message": 'johnsmith added you to Channel1_Public'
        }
    ]

    assert data_notifications_get == expected_data

# Testing for an invalid token
def test_invalid_token(reset_data, user1, user2, channel1):
    # Remove user2
    notifications_register = {
        "token": "INVALID_TOKEN",
    }    

    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    assert response_notifications_get.status_code == 403

# Testing for when there is an invalid tag
def test_invalid_tag(reset_data, user1, user2, channel1):
    
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@notjohnsmith hi',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    notifications_register = {
        "token": user1['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = []

    assert data_notifications_get == expected_data

# Testing for when a person is tagged but is not in the channel
def test_tagged_outside_channel(reset_data, user1, user2, user3, channel1):

    data_send_message = {
        'token' : user1['token'],
        'channel_id' : channel1['channel_id'],
        'message' : '@chriselvin hi',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    notifications_register = {
        "token": user2['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = []

    assert data_notifications_get == expected_data

# Testing for when a person is tagged but is not in the dm
def test_tagged_outside_dm(reset_data, user1, user2, user3):

    data = {
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']]
    }
    response = requests.post(
        f"{config.url}dm/create/v1",
        json=data
    )
    dm_id = response.json()['dm_id']
    
    data_send_message = {
        'token' : user1['token'],
        'dm_id' : dm_id,
        'message' : '@johnnyjacobs hi',
    }
    requests.post(
        f'{config.url}message/senddm/v1',
        json=data_send_message
    )

    notifications_register = {
        "token": user3['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = []

    assert data_notifications_get == expected_data

# Testing for when there are just normal messages with no tagging
def test_no_tagging(reset_data, user1, user2, channel1):
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : 'yo johnsmith what u up to',
    }
    requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    notifications_register = {
        "token": user1['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = []

    assert data_notifications_get == expected_data

# Testing for getting tagged in a share message
def test_share_tagged_notification(reset_data, user1, user2, channel1):
    pass

def test_edited_messaged(reset_data, user1, user2, channel1):
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(f"{config.url}channel/join/v2",\
    json=join_register)

    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : 'hi',
    }
    message = requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )
    
    message_id = message.json()['message_id']
    edited_message = "@johnsmith hi"

    data_edit_message = {
        "token": user2['token'],
        "message_id": message_id,
        "message": edited_message
    }

    #message/edit/v1
    requests.put(f"{config.url}message/edit/v1", \
        json=data_edit_message)

    notifications_register = {
        "token": user1['token']
    }
    response_notifications_get = requests.get(
        f'{config.url}notifications/get/v1',
        params=notifications_register
    )

    data_notifications_get = response_notifications_get.json()

    expected_data = [{
        "channel_id": channel1['channel_id'],
        "dm_id": -1,
        "notification_message": 'chriselvin tagged you in Channel1_Public: @johnsmith hi'
    }]

    assert data_notifications_get == expected_data
    