import pytest
from datetime import datetime, timezone, timedelta
import time 
import requests
from src import config

@pytest.fixture
def reset(): 
    requests.delete(f"{config.url}clear/v1")

    data_register = { 
        'email': "realemail_812@outlook.edu.au",
        'password': "Password1",
        'name_first': "John",
        'name_last': "Smith",
    }

    response_register = requests.post(f"{config.url}auth/register/v2", json=data_register)

    data_create = {
        'token': response_register.json()['token'],
        'name': "Channel1", 
        'is_public': True,
    }
    response_create = requests.post(f"{config.url}channels/create/v2", json=data_create)

    return {
        'user': response_register.json(), 
        'channel_id': response_create.json()['channel_id']
    }

def test_valid(reset): 
    # time_sent = current time + 3 seconds
    # send message after 3 secs
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlater = {
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'message': 'valid message', 
        'time_sent': time_sent,
    }

    response_sendlater = requests.post(f"{config.url}message/sendlater/v1", json=data_sendlater)
    assert type(response_sendlater.json()['message_id']) is int

    # sleep 2 seconds and make sure message isn't there yet
    time.sleep(2)
    data_messages = { 
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'start': 0, 
    }

    response_messages = requests.get(f"{config.url}channel/messages/v2", params=data_messages)
    assert response_messages.json() == {'messages' : [], 'start': 0, 'end': -1}

    # sleep extra 1.5 secs so roughly 3.5 secs total, and check to see if message is there
    time.sleep(1.5)
    data_messages = { 
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'start': 0, 
    }

    response_messages = requests.get(f"{config.url}channel/messages/v2", params=data_messages)
    
    channel_messages = response_messages.json()
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    assert abs(
        channel_messages['messages'][0]['time_created'] - current_time
    ) < 2

    # Checking the rest of the return
    expected = {
        'messages' : [
            {
                'message_id' : response_sendlater.json()['message_id'],
                'u_id' : reset['user']['auth_user_id'],
                'message' : 'valid message',
            }
        ],
        'start' : 0,
        'end' : -1,
    }
    # Removing time to check separately, index of 0 as there is only 1 message
    del channel_messages['messages'][0]['time_created']
    assert channel_messages == expected

def test_two_messages(reset): 
    # time_sent = current time + 3 seconds
    # send message 3 secs after
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlater = {
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'message': 'valid message', 
        'time_sent': time_sent,
    }

    response_sendlater_1 = requests.post(f"{config.url}message/sendlater/v1", json=data_sendlater)
    assert type(response_sendlater_1.json()['message_id']) is int

    # send another message 5 secs after
    time_sent_2 = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 5
    data_sendlater = {
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'message': 'its me again', 
        'time_sent': time_sent_2,
    }

    response_sendlater_2 = requests.post(f"{config.url}message/sendlater/v1", json=data_sendlater)
    assert type(response_sendlater_2.json()['message_id']) is int

    # sleep 2 seconds and make sure first and second messages aren't there yet
    time.sleep(2)
    data_messages = { 
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'start': 0, 
    }

    response_messages = requests.get(f"{config.url}channel/messages/v2", params=data_messages)
    assert response_messages.json() == {'messages' : [], 'start': 0, 'end': -1}

    # sleep extra 1.5 secs so roughly 3.5 secs total, and check to see if first message is there
    time.sleep(1.5)
    data_messages = { 
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'start': 0, 
    }

    response_messages = requests.get(f"{config.url}channel/messages/v2", params=data_messages)
    # check timing of message 1 
    channel_messages = response_messages.json()
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    assert abs(
        channel_messages['messages'][0]['time_created'] - current_time
    ) < 2

    # Checking the rest of the return
    expected = {
        'messages' : [
            {
                'message_id' : response_sendlater_1.json()['message_id'],
                'u_id' : reset['user']['auth_user_id'],
                'message' : 'valid message',
            }
        ],
        'start' : 0,
        'end' : -1,
    }
    # Removing time to check separately, index of 0 as there is only 1 message
    del channel_messages['messages'][0]['time_created']
    assert channel_messages == expected

    # sleep another 2 secs so roughly 5.5s total, check if second message is there
    time.sleep(2)

    response_messages = requests.get(f"{config.url}channel/messages/v2", params=data_messages)
    
    # check timing of 2nd message 
    channel_messages = response_messages.json()
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    assert abs(
        channel_messages['messages'][1]['time_created'] - current_time
    ) < 2

    # Checking the second message
    expected = {
        'messages' : [
            {
                'message_id' : response_sendlater_1.json()['message_id'],
                'u_id' : reset['user']['auth_user_id'],
                'message' : 'valid message',
            }, { 
                'message_id': response_sendlater_2.json()['message_id'], 
                'u_id': reset['user']['auth_user_id'], 
                'message': 'its me again',
            }
        ],
        'start' : 0,
        'end' : -1,
    }

    # Removing time to check separately, index both 0 and 1 for all messages
    del channel_messages['messages'][1]['time_created']
    del channel_messages['messages'][0]['time_created']
    assert channel_messages == expected

def test_invalid_channel_id(reset): 
    # time_sent = current time + 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlater = { 
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'] + 1, 
        'message': 'valid message', 
        'time_sent': time_sent, 
    }

    response_sendlater = requests.post(f"{config.url}message/sendlater/v1", json=data_sendlater)
    assert response_sendlater.status_code == 400

def test_message_too_long(reset): 
    # time_sent = current time + 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlater = { 
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'], 
        'message': 'x'*1001, 
        'time_sent': time_sent, 
    }
    response_sendlater = requests.post(f"{config.url}message/sendlater/v1", json=data_sendlater)
    assert response_sendlater.status_code == 400

def test_time_sent_in_past(reset): 
    # time_sent = current time - 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() - 3
    data_sendlater = { 
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'], 
        'message': 'valid message', 
        'time_sent': time_sent, 
    }

    response_sendlater = requests.post(f"{config.url}message/sendlater/v1", json=data_sendlater)
    assert response_sendlater.status_code == 400

def test_user_not_in_channel(reset): 
    # register a new user not in the channel
    data_register = { 
        'email': "realemail_813@outlook.edu.au",
        'password': "Password2",
        'name_first': "Jack",
        'name_last': "Chen",
    }

    response_register = requests.post(f"{config.url}auth/register/v2", json=data_register)


    # time_sent = current time + 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlater = { 
        'token': response_register.json()['token'], 
        'channel_id': reset['channel_id'], 
        'message': 'valid message', 
        'time_sent': time_sent, 
    }

    response_sendlater = requests.post(f"{config.url}message/sendlater/v1", json=data_sendlater)
    assert response_sendlater.status_code == 403

def test_invalid_token(reset): 
    # time_sent = current time + 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlater = { 
        'token': 'invalid_token', 
        'channel_id': reset['channel_id'], 
        'message': 'valid message', 
        'time_sent': time_sent, 
    }

    response_sendlater = requests.post(f"{config.url}message/sendlater/v1", json=data_sendlater)
    assert response_sendlater.status_code == 403


def test_send_message_before_sendlater(reset): 
    # CLARIFICATION: this test is meant to test the message_id's and their interaction
    # when a message is set to sendlater but another message is quickly sent 
    # before the message in sendlater has been sent 

    # time_sent = current time + 3 seconds
    # send a message after 3 secs
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlater = {
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'message': 'valid message', 
        'time_sent': time_sent,
    }

    response_sendlater = requests.post(f"{config.url}message/sendlater/v1", json=data_sendlater)
    assert type(response_sendlater.json()['message_id']) is int

    # send a quick message before prev message arrives
    data_send = {
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'message': 'quick message'
    }
    response_send = requests.post(f"{config.url}message/send/v1", json=data_send)

    data_messages = { 
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'start': 0, 
    }

    response_messages = requests.get(f"{config.url}channel/messages/v2", params=data_messages)
    
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    channel_messages = response_messages.json()
    
    # check timing of message 2
    assert abs(
        channel_messages['messages'][0]['time_created'] - current_time
    ) < 2

    # removing time of 2nd message
    del channel_messages['messages'][0]['time_created']


    quick_message = { 
        'message_id': response_send.json()['message_id'],
        'u_id': reset['user']['auth_user_id'], 
        'message': 'quick message'
    }

    assert channel_messages == {'messages' : [quick_message], 'start': 0, 'end': -1}

    # sleep for 3.5 secs and check if first message is there
    time.sleep(3.5)
    data_messages = { 
        'token': reset['user']['token'], 
        'channel_id': reset['channel_id'],
        'start': 0, 
    }

    response_messages = requests.get(f"{config.url}channel/messages/v2", params=data_messages)
    
    channel_messages = response_messages.json()
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    assert abs(
        channel_messages['messages'][1]['time_created'] - current_time
    ) < 2

    # Checking the rest of the return
    expected = {
        'messages' : [ quick_message,
            {
                'message_id' : response_sendlater.json()['message_id'],
                'u_id' : reset['user']['auth_user_id'],
                'message' : 'valid message',
            }, 
        ],
        'start' : 0,
        'end' : -1,
    }
    # Removing time of both 1st and 2nd message
    del channel_messages['messages'][0]['time_created']
    del channel_messages['messages'][1]['time_created']
    assert channel_messages == expected
