import requests
from src import config
from fake.util import parse_response

def admin_user_remove(token, u_id):
    res = requests.delete(
        f"{config.url}admin/user/remove/v1",
        json={
            'token' : token,
            'u_id' : u_id,
        }
    )
    return parse_response(res)

def admin_userpermission_change(token, u_id, permission_id):
    res = requests.post(
        f"{config.url}admin/userpermission/change/v1",
        json={
            'token' : token,
            'u_id' : u_id,
            'permission_id' : permission_id,
        }
    )
    return parse_response(res)
