import requests
from src import config
from fake.util import parse_response

def user_profile(token, u_id):
    res = requests.get(
        f"{config.url}user/profile/v1",
        params={
            'token' : token,
            'u_id' : u_id,
        }
    )
    return parse_response(res)

def user_profile_setname(token, name_first, name_last):
    res = requests.put(
        f"{config.url}user/profile/setname/v1",
        json={
            'token' : token,
            'name_first' : name_first,
            'name_last' : name_last,
        }
    )
    return parse_response(res)

def user_profile_setemail(token, email):
    res = requests.put(
        f"{config.url}user/profile/setemail/v1",
        json={
            'token' : token,
            'email' : email,
        }
    )
    return parse_response(res)

def user_profile_sethandle(token, handle_str):
    res = requests.put(
        f"{config.url}user/profile/sethandle/v1",
        json={
            'token' : token,
            'handle_str' : handle_str,
        }
    )
    return parse_response(res)

def user_stats(token):
    res = requests.get(
        f"{config.url}user/stats/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    res = requests.post(
        f"{config.url}user/profile/uploadphoto/v1",
        json={
            'token' : token, 
            'img_url' : img_url, 
            'x_start' : x_start, 
            'y_start' : y_start, 
            'x_end' : x_end, 
            'y_end' : y_end,
        }
    )
    return parse_response(res)
