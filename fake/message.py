import requests
from src import config
from fake.util import parse_response

def message_send(token, channel_id, message):
    res = requests.post(
        f"{config.url}message/send/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : message,
        }
    )
    return parse_response(res)

def message_edit(token, message_id, message):
    res = requests.put(
        f"{config.url}message/edit/v1",
        json={
            'token' : token,
            'message_id' : message_id,
            'message' : message,
        }
    )
    return parse_response(res)

def message_remove(token, message_id):
    res = requests.delete(
        f"{config.url}message/remove/v1",
        json={
            'token' : token,
            'message_id' : message_id,
        }
    )
    return parse_response(res)

def message_share(token, og_message_id, message, channel_id, dm_id):
    res = requests.post(
        f"{config.url}message/share/v1",
        json={
            'token' : token,
            'og_message_id' : og_message_id,
            'message' : message,
            'channel_id' : channel_id,
            'dm_id' : dm_id,
        }
    )
    return parse_response(res)

def message_react(token, message_id, react_id):
    res = requests.post(
        f"{config.url}message/react/v1",
        json={
            'token' : token,
            'message_id' : message_id,
            'react_id' : react_id,
        }
    )
    return parse_response(res)

def message_unreact(token, message_id, react_id):
    res = requests.post(
        f"{config.url}message/unreact/v1",
        json={
            'token' : token,
            'message_id' : message_id,
            'react_id' : react_id,
        }
    )
    return parse_response(res)

def message_pin(token, message_id):
    res = requests.post(
        f"{config.url}message/pin/v1",
        json={
            'token' : token,
            'message_id' : message_id,
        }
    )
    return parse_response(res)

def message_unpin(token, message_id):
    res = requests.post(
        f"{config.url}message/unpin/v1",
        json={
            'token' : token,
            'message_id' : message_id,
        }
    )
    return parse_response(res)

def message_sendlater(token, channel_id, message, time_sent):
    res = requests.post(
        f"{config.url}message/sendlater/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : message,
            'time_sent' : time_sent,
        }
    )
    return parse_response(res)

def message_sendlaterdm(token, dm_id, message, time_sent):
    res = requests.post(
        f"{config.url}message/sendlaterdm/v1",
        json={
            'token' : token,
            'dm_id' : dm_id,
            'message' : message,
            'time_sent' : time_sent,
        }
    )
    return parse_response(res)