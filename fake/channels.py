import requests
from src import config
from fake.util import parse_response

def channels_create(token, name, is_public):
    res = requests.post(
        f"{config.url}channels/create/v2",
        json={
            'token' : token,
            'name' : name,
            'is_public' : is_public,
        }
    )
    return parse_response(res)

def channels_list(token):
    res = requests.get(
        f"{config.url}channels/list/v2",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

def channels_listall(token):
    res = requests.get(
        f"{config.url}channels/listall/v2",
        params={
            'token' : token,
        }
    )
    return parse_response(res)