import requests
from src import config
from fake.util import parse_response

def clear():
    response = requests.delete(
        f'{config.url}clear/v1',
    )
    return parse_response(response)