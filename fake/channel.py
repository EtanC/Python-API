import requests
from src import config
from fake.util import parse_response

def channel_details(token, channel_id):
    res = requests.get(
        f"{config.url}channel/details/v2",
        params={
            'token' : token,
            'channel_id' : channel_id,
        }
    )
    return parse_response(res)

def channel_join(token, channel_id):
    res = requests.post(
        f"{config.url}channel/join/v2",
        json={
            'token' : token,
            'channel_id' : channel_id,
        }
    )
    return parse_response(res)

def channel_invite(token, channel_id, u_id):
    res = requests.post(
        f"{config.url}channel/invite/v2",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'u_id' : u_id,
        }
    )
    return parse_response(res)

def channel_messages(token, channel_id, start):
    res = requests.get(
        f"{config.url}channel/messages/v2",
        params={
            'token' : token,
            'channel_id' : channel_id,
            'start' : start,
        }
    )
    return parse_response(res)

def channel_leave(token, channel_id):
    res = requests.post(
        f"{config.url}channel/leave/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
        }
    )
    return parse_response(res)

def channel_addowner(token, channel_id, u_id):
    res = requests.post(
        f"{config.url}channel/addowner/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'u_id' : u_id,
        }
    )
    return parse_response(res)

def channel_removeowner(token, channel_id, u_id):
    res = requests.post(
        f"{config.url}channel/removeowner/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'u_id' : u_id,
        }
    )
    return parse_response(res)