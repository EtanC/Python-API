import pytest
from datetime import datetime, timezone
import time 
import requests
from src import config

@pytest.fixture
def reset():
    requests.delete(f"{config.url}clear/v1")
    
    # creator of dm
    data_register = { 
        'email': "realemail_812@outlook.edu.au",
        'password': "Password1",
        'name_first': "John",
        'name_last': "Smith",
    }

    response_register = requests.post(f"{config.url}auth/register/v2", json=data_register)
    creator_data = response_register.json()
    
    # receiver of dm 
    data_register = {
        'email': "realemail_813@outlook.edu.au",
        'password': "Password2",
        'name_first': "Jack",
        'name_last': "Chen",
    }
    response_register = requests.post(f"{config.url}auth/register/v2", json=data_register)
    receiver_data = response_register.json()
    
    data_dm = {
        'token': creator_data['token'],
        'u_ids': [receiver_data['auth_user_id']]
    }
    response_dm = requests.post(f"{config.url}dm/create/v1", json=data_dm)
    dm_data = response_dm.json()
    
    return {
        'creator': creator_data,
        'receiver': receiver_data, 
        'dm_id': dm_data['dm_id'],
    }

def test_valid(reset): 
    # time_sent = current time + 3 seconds
    # send dm after 3 secs
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    
    # creator of dm requests sendlaterdm
    data_sendlaterdm = {
        'token': reset['creator']['token'],
        'dm_id': reset['dm_id'], 
        'message': '',
        'time_sent': time_sent,
    }
    response_sendlaterdm = requests.post(f"{config.url}message/sendlaterdm/v1", json=data_sendlaterdm)
    # checking type of message_id returned is correct
    assert type(response_sendlaterdm.json()['message_id']) is int 
    
    # sleep 2 seconds and make sure message isn't there yet
    time.sleep(2)
    data_dm = { 
        'token': reset['creator']['token'], 
        'dm_id': reset['dm_id'],
        'start': 0, 
    }
    response_dm = requests.get(f"{config.url}dm/messages/v1", params=data_dm)
    assert response_dm.json() == {
        'messages': [],
        'start': 0, 
        'end': -1
    }
    
    
    # sleep extra 1.5 secs so roughly 3.5 secs total, and check to see if message is there
    time.sleep(1.5)
    response_dm = requests.get(f"{config.url}dm/messages/v1", params=data_dm)
    dm_messages = response_dm.json() 
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    # check timing of dm sent
    assert abs(
        dm_messages['messages'][0]['time_created'] - current_time
    ) < 2
    
    # Checking the rest of the return
    expected = {
        'messages' : [
            {
                'message_id' : response_sendlaterdm.json()['message_id'],
                'u_id' : reset['creator']['auth_user_id'],
                'message' : '',
            }
        ],
        'start' : 0,
        'end' : -1,
    }
    
    # remove time created in dm, as it won't be the same as the one recorded
    # just then, there'll be a small difference that can't be avoided
    del dm_messages['messages'][0]['time_created']
    assert dm_messages == expected


def test_two_dms(reset): 
    # time_sent = current time + 3 seconds
    # send dm 3 secs after
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlaterdm = {
        'token': reset['creator']['token'], 
        'dm_id': reset['dm_id'],
        'message': 'valid message', 
        'time_sent': time_sent,
    }

    response_sendlaterdm_1 = requests.post(f"{config.url}message/sendlaterdm/v1", json=data_sendlaterdm)
    assert type(response_sendlaterdm_1.json()['message_id']) is int

    # send another dm 5 secs after
    time_sent_2 = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 5
    data_sendlater = {
        'token': reset['creator']['token'], 
        'dm_id': reset['dm_id'],
        'message': 'its me again', 
        'time_sent': time_sent_2,
    }

    response_sendlaterdm_2 = requests.post(f"{config.url}message/sendlaterdm/v1", json=data_sendlater)
    assert type(response_sendlaterdm_2.json()['message_id']) is int

    # sleep 2 seconds and make sure first and second dms aren't there yet
    time.sleep(2)
    data_dm = { 
        'token': reset['creator']['token'], 
        'dm_id': reset['dm_id'],
        'start': 0, 
    }

    response_dm = requests.get(f"{config.url}dm/messages/v1", params=data_dm)
    assert response_dm.json() == {'messages' : [], 'start': 0, 'end': -1}

    # sleep extra 1.5 secs so roughly 3.5 secs total, and check to see if first dm is there
    time.sleep(1.5)

    response_dm = requests.get(f"{config.url}dm/messages/v1", params=data_dm)
    
    # check timing of dm 1 
    dm_messages = response_dm.json()
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    assert abs(
        dm_messages['messages'][0]['time_created'] - current_time
    ) < 2

    # Checking the rest of the return
    expected = {
        'messages' : [
            {
                'message_id' : response_sendlaterdm_1.json()['message_id'],
                'u_id' : reset['creator']['auth_user_id'],
                'message' : 'valid message',
            }
        ],
        'start' : 0,
        'end' : -1,
    }
    # Removing time to check separately, index of 0 as there is only 1 dm
    del dm_messages['messages'][0]['time_created']
    assert dm_messages == expected

    # sleep another 2 secs so roughly 5.5s total, check if second dm is there
    time.sleep(2)

    response_dm = requests.get(f"{config.url}dm/messages/v1", params=data_dm)
    
    # check timing of 2nd message 
    dm_messages = response_dm.json()
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    assert abs(
        dm_messages['messages'][1]['time_created'] - current_time
    ) < 2

    # Checking the second message
    expected = {
        'messages' : [
            {
                'message_id' : response_sendlaterdm_1.json()['message_id'],
                'u_id' : reset['creator']['auth_user_id'],
                'message' : 'valid message',
            }, { 
                'message_id': response_sendlaterdm_2.json()['message_id'], 
                'u_id': reset['creator']['auth_user_id'], 
                'message': 'its me again',
            }
        ],
        'start' : 0,
        'end' : -1,
    }

    # Removing time to check separately, index both 0 and 1 for all messages
    del dm_messages['messages'][1]['time_created']
    del dm_messages['messages'][0]['time_created']
    assert dm_messages == expected

def test_invalid_dm_id(reset): 
    # time_sent = current time + 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlaterdm = { 
        'token': reset['creator']['token'], 
        'dm_id': reset['dm_id'] + 1, 
        'message': 'valid message', 
        'time_sent': time_sent, 
    }

    response_sendlaterdm = requests.post(f"{config.url}message/sendlaterdm/v1", json=data_sendlaterdm)
    assert response_sendlaterdm.status_code == 400

def test_long_message(reset):
    # time_sent = current time + 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlaterdm = { 
        'token': reset['creator']['token'], 
        'dm_id': reset['dm_id'], 
        'message': 'x'*1001, 
        'time_sent': time_sent, 
    }
    response_sendlaterdm = requests.post(f"{config.url}message/sendlaterdm/v1", json=data_sendlaterdm)
    assert response_sendlaterdm.status_code == 400

def test_time_sent_in_past(reset): 
    # time_sent = current time - 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() - 3
    data_sendlaterdm = { 
        'token': reset['creator']['token'], 
        'dm_id': reset['dm_id'], 
        'message': 'valid message', 
        'time_sent': time_sent, 
    }

    response_sendlaterdm = requests.post(f"{config.url}message/sendlaterdm/v1", json=data_sendlaterdm)
    assert response_sendlaterdm.status_code == 400

def test_user_not_in_dm(reset): 
    # register a new user not in the dm
    data_register = { 
        'email': "realemail_814@outlook.edu.au",
        'password': "Password3",
        'name_first': "Bob",
        'name_last': "Chen",
    }

    response_register = requests.post(f"{config.url}auth/register/v2", json=data_register)


    # time_sent = current time + 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlater = { 
        'token': response_register.json()['token'], 
        'dm_id': reset['dm_id'], 
        'message': 'valid message', 
        'time_sent': time_sent, 
    }

    response_sendlater = requests.post(f"{config.url}message/sendlaterdm/v1", json=data_sendlater)
    assert response_sendlater.status_code == 403

def test_invalid_token(reset):
    # time_sent = current time + 3 seconds
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlaterdm = { 
        'token': 'invalid_token', 
        'channel_id': reset['channel_id'], 
        'message': 'valid message', 
        'time_sent': time_sent, 
    }

    response_sendlaterdm = requests.post(f"{config.url}message/sendlaterdm/v1", json=data_sendlaterdm)
    assert response_sendlaterdm.status_code == 403


def test_send_dm_before_sendlaterdm(reset): 
    # CLARIFICATION: this test is meant to test the message_id's and their interaction
    # when a dm is set to sendlaterdm but another dm is quickly sent 
    # before the dm in sendlaterdm has been sent 

    # time_sent = current time + 3 seconds
    # send a dm after 3 secs
    time_sent = datetime.now().replace(tzinfo=timezone.utc).timestamp() + 3
    data_sendlaterdm = {
        'token': reset['creator']['token'], 
        'dm_id': reset['dm)id'],
        'message': 'valid message', 
        'time_sent': time_sent,
    }

    response_sendlaterdm = requests.post(f"{config.url}message/sendlaterdm/v1", json=data_sendlaterdm)
    assert type(response_sendlaterdm.json()['message_id']) is int

    # send a quick message before prev message arrives
    data_senddm = {
        'token': reset['creator']['token'], 
        'dm_id': reset['dm_id'],
        'message': 'quick message'
    }
    response_senddm = requests.post(f"{config.url}message/senddm/v1", json=data_senddm)

    data_dm_messages = { 
        'token': reset['creator']['token'], 
        'dm_id': reset['dm_id'],
        'start': 0, 
    }

    response_dm_messages = requests.get(f"{config.url}dm/messages/v1", params=data_dm_messages)
    
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    dm_messages = response_dm_messages.json()
    
    # check timing of dm 2
    assert abs(
        dm_messages['messages'][0]['time_created'] - current_time
    ) < 2

    # removing time of 2nd dm
    del dm_messages['messages'][0]['time_created']


    quick_dm = { 
        'message_id': response_senddm.json()['message_id'],
        'u_id': reset['creator']['auth_user_id'], 
        'message': 'quick message'
    }

    assert dm_messages == {'messages' : [quick_dm], 'start': 0, 'end': -1}

    # sleep for 3.5 secs and check if first message is there
    time.sleep(3.5)

    response_dm_messages = requests.get(f"{config.url}channel/messages/v2", params=data_dm_messages)
    
    dm_messages = response_dm_messages.json()
    current_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    # check timing of 1st message
    assert abs(
        dm_messages['messages'][1]['time_created'] - current_time
    ) < 2

    # Checking the rest of the return
    expected = {
        'messages' : [ quick_dm,
            {
                'message_id' : response_sendlaterdm.json()['message_id'],
                'u_id' : reset['creator']['auth_user_id'],
                'message' : 'valid message',
            }, 
        ],
        'start' : 0,
        'end' : -1,
    }
    # Removing time of both 1st and 2nd dm's
    del dm_messages['messages'][0]['time_created']
    del dm_messages['messages'][1]['time_created']
    assert dm_messages == expected
