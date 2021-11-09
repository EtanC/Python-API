import requests
from src import config
from fake.util import parse_response

def dm_create(token, u_ids):
    res = requests.post(
        f"{config.url}dm/create/v1",
        json={
            'token' : token,
            'u_ids' : u_ids,
        }
    )
    return parse_response(res)

def dm_list(token):
    res = requests.get(
        f"{config.url}dm/list/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

def dm_remove(token, dm_id):
    res = requests.delete(
        f"{config.url}dm/remove/v1",
        json={
            'token' : token,
            'dm_id' : dm_id,
        }
    )
    return parse_response(res)

def dm_details(token, dm_id):
    res = requests.get(
        f"{config.url}dm/details/v1",
        params={
            'token' : token,
            'dm_id' : dm_id,
        }
    )
    return parse_response(res)

def dm_leave(token, dm_id):
    res = requests.post(
        f"{config.url}dm/leave/v1",
        json={
            'token' : token,
            'dm_id' : dm_id,
        }
    )
    return parse_response(res)

def dm_messages(token, dm_id, start):
    res = requests.get(
        f"{config.url}dm/messages/v1",
        params={
            'token' : token,
            'dm_id' : dm_id,
            'start' : start,
        }
    )
    return parse_response(res)

def message_senddm(token, dm_id, message):
    res = requests.post(
        f"{config.url}message/senddm/v1",
        json={
            'token' : token,
            'dm_id' : dm_id,
            'message' : message,
        }
    )
    return parse_response(res)
