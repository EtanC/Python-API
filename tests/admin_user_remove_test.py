import pytest 
import requests
from src import config 
from datetime import datetime, timezone
from src.helper import current_timestamp

@pytest.fixture
def reset_data():
    requests.delete(f"{config.url}clear/v1")

# User 1 (global user)
@pytest.fixture
def user1():
    user1_register = {
        'email': "john.smith@gmail.com",
        'password': "password1",
        'name_first': "John",
        'name_last': "Smith",
    }

    response_user1_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user1_register
    )

    auth_user_id = response_user1_register.json()['auth_user_id']
    token        = response_user1_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# User 2 (normal user)
@pytest.fixture
def user2():
    user2_register = {
        'email': "chris.elvin@gmail.com",
        'password': "password2",
        'name_first': "Chris",
        'name_last': "Elvin",
    }

    response_user2_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user2_register
    )

    auth_user_id = response_user2_register.json()['auth_user_id']
    token        = response_user2_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# User 3 (normal user)
@pytest.fixture
def user3():
    user3_register = {
        'email': "sam.ross@gmail.com",
        'password': "password3",
        'name_first': "Sam",
        'name_last': "Ross",
    }

    response_user3_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user3_register
    )

    auth_user_id = response_user3_register.json()['auth_user_id']
    token        = response_user3_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# create private channel called channel2 where user1 will be added
@pytest.fixture
def channel1(user1):

    channel1_register = {
        'token': user1['token'],
        'name': "Channel1",
        'is_public': True,
    }

    response_channel1_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel1_register
    )

    channel_id = response_channel1_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

def test_channel_remove(reset_data, user1, user2, channel1):

    # User2 join channel
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(
        f"{config.url}channel/join/v2", json=join_register
    )

    user_remove_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id']
    }

    requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    details_register = {
        "token": user1['token'],
        "channel_id": channel1['channel_id']
    }

    response_details_register = requests.get(
        f"{config.url}channel/details/v2", params=details_register
    )

    response_details_data = response_details_register.json()

    owner_members = [
        {
            'u_id': channel1['user_id'], 
            'email': "john.smith@gmail.com", 
            'name_first': "John", 
            'name_last': "Smith", 
            'handle_str': "johnsmith",
        }
    ]

    all_members = [
        {
            'u_id': channel1['user_id'], 
            'email': "john.smith@gmail.com", 
            'name_first': "John", 
            'name_last': "Smith", 
            'handle_str': "johnsmith",
        }
    ]

    expected_data = {
        "name": "Channel1",
        "is_public": True,
        "owner_members": owner_members,
        "all_members": all_members,
    }
    del response_details_data['owner_members'][0]['profile_img_url']
    del response_details_data['all_members'][0]['profile_img_url']
    assert response_details_data == expected_data

def test_channel_remove_owner(reset_data, user1, user2, channel1):

    # User2 join channel
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(
        f"{config.url}channel/join/v2", json=join_register
    )

    # Change user2 into global owner
    userpermission_change_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id'],
        "permission_id": 1
    }

    requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    user_remove_register = {
        "token": user2['token'],
        "u_id": user1['auth_user_id']
    }

    requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    details_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    response_details_register = requests.get(
        f"{config.url}channel/details/v2", params=details_register
    )

    response_details_data = response_details_register.json()

    owner_members = []

    all_members = [
        {
            'u_id': user2['auth_user_id'], 
            'email': 'chris.elvin@gmail.com', 
            'name_first': 'Chris', 
            'name_last': 'Elvin', 
            'handle_str': 'chriselvin', 
        }
    ]

    expected_data = {
        "name": "Channel1",
        "is_public": True,
        "owner_members": owner_members,
        "all_members": all_members,
    }
    del response_details_data['all_members'][0]['profile_img_url']
    assert response_details_data == expected_data

def test_dm_remove(reset_data, user1, user2):

    # User1 create dm
    dm_create_register = {
        "token": user1['token'],
        "u_ids":[user1['auth_user_id'], user2['auth_user_id']]
    }

    requests.post(
        f"{config.url}dm/create/v1", json=dm_create_register
    )

    user_remove_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id']
    }

    requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    dm_list_register = {
        "token": user2['token']
    }

    response_dm_list_register = requests.get(
        f"{config.url}dm/list/v1", params=dm_list_register
    )

    response_dm_list_data = response_dm_list_register.json()

    expected_data = {'dms':[]}

    assert response_dm_list_data == expected_data

def test_remove_original_owner(reset_data, user1, user2):

    # Change user2 into global owner
    userpermission_change_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id'],
        "permission_id": 1
    }

    requests.post(
        f"{config.url}admin/userpermission/change/v1", json=userpermission_change_register
    )

    user_remove_register = {
        "token": user2['token'],
        "u_id": user1['auth_user_id']
    }

    requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    users_all_register = {
        "token": user2['token']
    }

    response_users_all_register = requests.get(
        f"{config.url}users/all/v1", params=users_all_register
    )

    users_all_data = response_users_all_register.json()

    expected_data = {'users': [{
        'u_id': user2['auth_user_id'], 
        'email': 'chris.elvin@gmail.com', 
        'name_first': 'Chris', 
        'name_last': 'Elvin', 
        'handle_str': 'chriselvin', 
    }]}
    del users_all_data['users'][0]['profile_img_url']
    assert users_all_data == expected_data

def test_channel_messages_remove(reset_data, user1, user2, channel1):
    
    # User2 join channel
    join_register = {
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    }

    requests.post(
        f"{config.url}channel/join/v2", json=join_register
    )

    data_send_message = {
        'token' : user2['token'],
        'channel_id' : channel1['channel_id'],
        'message' : 'hi',
    }
    response_send_message = requests.post(
        f'{config.url}message/send/v1',
        json=data_send_message
    )

    user_remove_register = {    
        "token": user1['token'],
        "u_id": user2['auth_user_id']
    }
    requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    data_messages = {
        'token' : user1['token'],
        'channel_id' : channel1['channel_id'],
        'start' : 0,
    }
    response_messages = requests.get(
        f'{config.url}channel/messages/v2',
        params=data_messages
    )
    # Checking time stamp
    channel_messages = response_messages.json()
    current_time = current_timestamp()
    assert abs(
        channel_messages['messages'][0]['time_created'] - current_time
    ) < 2
    # Checking the rest of the return
    expected = {
        'messages' : [
            {
                'message_id' : response_send_message.json()['message_id'],
                'u_id' : user2['auth_user_id'],
                'message' : 'Removed user',
                'is_pinned' : False
            }
        ],
        'start' : 0,
        'end' : -1,
    }
    # Removing time to check separately, index of 0 as there is only 1 message
    del channel_messages['messages'][0]['time_created']
    del channel_messages['messages'][0]['reacts']
    assert channel_messages == expected

def test_dm_messages_remove(reset_data, user1, user2):

    # User1 create dm
    dm_create_register = {
        "token": user1['token'],
        "u_ids":[user1['auth_user_id'], user2['auth_user_id']]
    }

    response_dm_create = requests.post(
        f"{config.url}dm/create/v1", json=dm_create_register
    )

    data = {
        'token' : user2['token'], 
        'dm_id' : response_dm_create.json()['dm_id'],
        'message' : 'I just sent a message lol xd'
    }
    response_send = requests.post(
        f"{config.url}message/senddm/v1",
        json=data
    )

    user_remove_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id']
    }
    requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    data = {
        'token': user1['token'], 
        'dm_id': response_dm_create.json()['dm_id'],
        'start': 0
    }
    response = requests.get(
        f"{config.url}dm/messages/v1",
        params=data
    )

    message = response.json()
    message_id = response_send.json()['message_id']

    # making sure that the time is within 2 seconds of each other
    time_current = current_timestamp()

    assert abs(
        message['messages'][0]['time_created'] - time_current
    ) < 2

    del message['messages'][0]['time_created']
    del message['messages'][0]['reacts']
    assert message == \
        {
            'messages' : [{
                'message': 'Removed user', 
                'message_id': message_id,
                'u_id': user2['auth_user_id'],
                'is_pinned' : False
            }],
            'start' : 0,
            'end' : -1
        }


def test_user_details_remove(reset_data, user1, user2):

    # Remove user2
    user_remove_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id']
    }

    requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    users_profile_register = {
        "token": user1['token'],
        "u_id": user2['auth_user_id']
    }

    response_user_profile_register = requests.get(
        f"{config.url}user/profile/v1", params=users_profile_register
    )

    user_profile_data = response_user_profile_register.json()

    expected_data = {'user': {
        'u_id': user2['auth_user_id'], 
        'email': None, 
        'name_first': 'Removed', 
        'name_last': 'user', 
        'handle_str': None, 
    }}
    del user_profile_data['user']['profile_img_url']
    assert user_profile_data == expected_data
    

def test_invalid_u_id(reset_data, user1, user2):

    # Remove invalid user
    user_remove_register = {
        "token": user1['token'],
        "u_id": user1['auth_user_id'] + user2['auth_user_id'] + 1,
    }    

    response_user_remove = requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    assert response_user_remove.status_code == 400

def test_only_global_owner(reset_data, user1):

    # Remove user1
    user_remove_register = {
        "token": user1['token'],
        "u_id": user1['auth_user_id'],
    }    

    response_user_remove = requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    assert response_user_remove.status_code == 400

def test_not_global_owner(reset_data, user1, user2):

    # Remove user2
    user_remove_register = {
        "token": user2['token'],
        "u_id": user2['auth_user_id'],
    }    

    response_user_remove = requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    assert response_user_remove.status_code == 403

def test_invalid_token(reset_data, user1, user2):

    # Remove user2
    user_remove_register = {
        "token": "INVALID_TOKEN",
        "u_id": user2['auth_user_id'],
    }    

    response_user_remove = requests.delete(
        f"{config.url}admin/user/remove/v1", json=user_remove_register
    )

    assert response_user_remove.status_code == 403