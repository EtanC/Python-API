from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper import token_to_user, get_user, decode_token

def notifications_get_v1(token):

    store = data_store.get()

    notifications = [{
        "channel_id": 0, 
        "dm_id": 0,
        "notification_message": ''
    }]

    token_data = decode_token(token)

    if (token_data is None) or ('auth_user_id' not in token_data): 
        raise AccessError(description='Invalid token')



    pass