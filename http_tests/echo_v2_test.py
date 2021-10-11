import requests
from src import config

def test_echo_valid():
    payload = {'data': 'hello'}
    response = requests.get(f"{config.url}/echo", params=payload)
    assert response.json() == {'data': 'hello'}

def test_echo_invalid():
    payload = {'data': 'echo'}
    response = requests.get(f"{config.url}/echo", params=payload)
    assert response.status_code == 400