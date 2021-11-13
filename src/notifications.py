from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper import token_to_user, get_user, decode_token

def notifications_get_v1(token):

    store = data_store.get()

    user = token_to_user(token, store)
    if user is None:
        raise AccessError(description='Invalid token')
    auth_user_id = user['u_id']

    for users in store['users']:
        if auth_user_id == users['u_id']:
            notifications = users['notifications'][0:20]

    return notifications