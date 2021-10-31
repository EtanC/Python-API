import requests
from src import config
from fake.util import parse_response

def search(token, query_str):
    res = requests.get(
        f"{config.url}search/v1",
        params={
            'token' : token,
            'query_str' : query_str,
        }
    )
    return parse_response(res)