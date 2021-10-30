import requests
from src import config
from fake.util import parse_response

def standup_start(token, channel_id, length):
    res = requests.post(
        f"{config.url}standup/start/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'length' : length,
        }
    )
    return parse_response(res)

def standup_active(token, channel_id):
    res = requests.get(
        f"{config.url}standup/active/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
        }
    )
    return parse_response(res)

def standup_send(token, channel_id, message):
    res = requests.post(
        f"{config.url}standup/send/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : message,
        }
    )
    return parse_response(res)
