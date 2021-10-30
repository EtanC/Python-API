import requests
from src import config
from fake.util import parse_response

def notifications_get(token):
    res = requests.get(
        f"{config.url}notifications/get/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)
