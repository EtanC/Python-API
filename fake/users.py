import requests
from src import config
from fake.util import parse_response

def users_all(token):
    res = requests.get(
        f"{config.url}users/all/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

def users_stats(token):
    res = requests.get(
        f"{config.url}users/stats/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)
