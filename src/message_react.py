from _pytest.monkeypatch import V
from src.data_store import data_store
from src.error import InputError
from src.error import AccessError
from src.helper import token_to_user, get_message, get_user

def message_react_v1(token, message_id, react_id): 
    store = data_store.get()

    # check token validity
    if token_to_user(token, store) is not None:
        user_id = token_to_user(token,store)['u_id']
    else: 
        raise AccessError(description='Invalid token') 

    user_react = token_to_user(token,store)

    # check message ID validity:
    if get_message(message_id, store) is not None:
        message = get_message(message_id, store)
    else: 
        raise InputError(description="Message ID is INVALID")
    
    # check if react_id ia valid. 
    if react_id is None or react_id != 1: 
        raise InputError(description="React_id is invalid")

    # check if user has already reacted it 
    for id in message['reacts'][0]['u_ids']:
        if user_id == id:
            raise InputError(description="User already reacted")

    # append the reacted person to the user list
    message['reacts'][0]['u_ids'].append(user_id)

    for channels in store['channels']:
        for messages in channels['messages']:
            if messages['message_id'] == message['message_id']:
                channel_name = channels['name']
                channel_id = channels['channel_id']
    
    user = get_user(message['u_id'], store)
    user['notifications'].insert(0, 
        {
        "channel_id": channel_id,
        "dm_id": -1,
        "notification_message": f'{user_react["handle_str"]} reacted to your message in {channel_name}'
        }
    )

    data_store.set(store)

    return {}

def message_unreact_v1(token, message_id, react_id): 
    store = data_store.get()

    # check token validity
    if token_to_user(token, store) is not None:
        user_id = token_to_user(token,store)['u_id']
    else: 
        raise AccessError(description='Invalid token')

    # check message ID validity:
    if get_message(message_id, store) is not None:
        message = get_message(message_id, store)
    else: 
        raise InputError(description="Message ID is INVALID")
    
    # check if react_id ia valid. 
    if react_id is None or react_id != 1: 
        raise InputError(description="react_id is invalid")

    # if it have not reacted yet
    reacted = False
    for id in message['reacts'][0]['u_ids']:
        if user_id == id:
            reacted = True
    if not reacted: 
        raise InputError(description="User has reacted")
    else: 
        message['reacts'][0]['u_ids'].remove(user_id)

    data_store.set(store)

    return {}
