import requests
from src import config
from fake.util import parse_response

def auth_login(email, password):
    response = requests.post(
        f"{config.url}auth/login/v2",
        json={'email' : email, 'password' : password}
    )
    return parse_response(response)

def auth_register(email, password, name_first, name_last):
    res = requests.post(
        f"{config.url}auth/register/v2",
        json={
            'email' : email,
            'password' : password,
            'name_first' : name_first,
            'name_last' : name_last,
        }
    )
    return parse_response(res)

def auth_logout(token):
    res = requests.post(
        f"{config.url}auth/logout/v1",
        json={
            'token' : token,
        }
    )
    return parse_response(res)

def auth_passwordreset_request(email):
    res = requests.post(
        f"{config.url}auth/passwordreset/request/v1",
        json={
            'email' : email,
        }
    )
    return parse_response(res)

def auth_passwordreset_reset(reset_code, new_password):
    res = requests.post(
        f"{config.url}auth/passwordreset/reset/v1",
        json={
            'reset_code' : reset_code,
            'new_password' : new_password,
        }
    )
    return parse_response(res)
