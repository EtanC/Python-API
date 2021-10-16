import pytest
import requests
import json
from src.channels import channels_create_v1, channels_create_v2

from src import config
'''
port = 8080
url = f"http://localhost:{port}/"
'''

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clearmessage/v1")

def test_():
    pass

#EXAMPLE:
'''
def test_invalid_email_register(reset_data):
    data_register = {
        "email": "uhh, im also a real email?",
        "password": "asdfghjkl",
        "name_first": "Bill",
        "name_last": "Thompson",
    }
    response_register = requests.post(f"{config.url}auth/register/v2",json=data_register)
    assert response_register.status_code == 400
'''

def test_invalid_length_message(reset_data): #POST

    # <1 length message
    data_register = {
        "token": "TOKEN",
        "channel_id": 0,
        "message": "",
    }
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 400

    # >1000 length message
    data_register['message'] = 'x' * 1001
    response_register = requests.post(f"{config.url}message/send/v1",\
    json=data_register)
    assert response_register.status_code == 400

def test_invalid_channelID_message(reset_data): #POST

    # get channel_id from channels/create/v2 (returns that)
    # channel_id = channels_details_v2(token, name, is_public)
    # data_register = {
    #    "token": "TOKEN",
    #    "message": "valid_message",
    # }
    # data_register.update(channel_id) 
    # invalid channel ID
    # response_register = requests.post(f"{config.url}message/send/v1",\
    # json=data_register)
    # assert response_register.status_code == 400

    pass

def test_nonmember_channel_message(reset_data):
    pass







'''
def test_heroes():
    response = requests.get(f'{BASE_URL}/heroes')
    response_data = response.json()
    assert response_data[0]['id'] == 0
    assert response_data[0]['name'] == "Superman"
'''


'''
message/send/v1: POST
    Input error:
    -channel_id does not refer to a valid channel
    -length of message is <1 or >1000 characters

    Access error:
    -channel_id is valid and the authorised user 
    is not a member of the channel
'''
'''
message/edit/v1:
    Input error:
    -length of message is over 1000 characters
    -message_id does not refer to a valid message within 
    a channel/DM that the authorised user has joined

    Access error:
    -message_id refers to a valid message in a 
    joined channel/DM and none of the following are true:
        .the message was sent by the authorised user making this request
        .the authorised user has owner permissions in the channel/DM

'''



