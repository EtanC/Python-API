import pytest
import requests
from src import config

@pytest.fixture
def reset():
    requests.delete(f"{config.url}clear/v1")

# CREATING TWO USERS NEED FOR THE INVITE

# User 1
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

# User 2
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

# User 3
@pytest.fixture
def user3():
    user3_register = {
        'email': "john.fort@gmail.com",
        'password': "password3",
        'name_first': "John",
        'name_last': "Fort",
    }

    response_user3_register = requests.post(
        f"{config.url}auth/register/v2",
        json=user3_register
    )

    auth_user_id = response_user3_register.json()['auth_user_id']
    token        = response_user3_register.json()['token']

    return {'token' : token, 'auth_user_id' : auth_user_id}

# Channel creation
@pytest.fixture
def channel(user1):

    channel_register = {
        'token': user1['token'],
        'name': "Channel",
        'is_public': True,
    }

    response_channel_register = requests.post(
        f"{config.url}channels/create/v2",
        json=channel_register
    )

    channel_id = response_channel_register.json()['channel_id']
    user_id    = user1['auth_user_id']

    return {'user_id' : user_id, 'channel_id' : channel_id}

def test_valid(reset, channel, user1, user2):

    # input parameters for channel_invite_v2
    invite_register = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user2['auth_user_id']
    }

    # invite user2 to the channel
    requests.post(
        f"{config.url}channel/invite/v2", json=invite_register
    )

    # retrieve channel details
    response_invite_register = requests.get(
        f"{config.url}channel/details/v2", params=invite_register
    )

    response_invite_register_data = response_invite_register.json()

    owner_members = [
        {
            'u_id': user1['auth_user_id'], 
            'email': "john.smith@gmail.com", 
            'name_first': "John", 
            'name_last': "Smith", 
            'handle_str': "johnsmith",
        }
    ]

    all_members = [
        {
            'u_id': user1['auth_user_id'], 
            'email': "john.smith@gmail.com", 
            'name_first': "John", 
            'name_last': "Smith", 
            'handle_str': "johnsmith",
        },

        {
            'u_id': user2['auth_user_id'], 
            'email': "chris.elvin@gmail.com", 
            'name_first': "Chris", 
            'name_last': "Elvin", 
            'handle_str': "chriselvin",
        }
    ]

    expected_data = {
        "name": "Channel",
        "is_public": True,
        "owner_members": owner_members,
        "all_members": all_members,
    }
    del response_invite_register_data['owner_members'][0]['profile_img_url']
    del response_invite_register_data['all_members'][0]['profile_img_url']
    del response_invite_register_data['all_members'][1]['profile_img_url']
    assert response_invite_register_data == expected_data


def test_invalid_channel(reset, channel, user1, user2):

    # input parameters for channel_invite_v2
    invite_register = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user2['auth_user_id']
    }

    invite_register['channel_id'] += 1

    response_invite_register = requests.post(f"{config.url}channel/invite/v2",\
    json=invite_register)
    assert response_invite_register.status_code == 400

def test_invalid_u_id(reset, channel, user1, user2):

    # input parameters for channel_invite_v2
    invite_register = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user1['auth_user_id'] + user2['auth_user_id'] + 1
    }

    response_invite_register = requests.post(f"{config.url}channel/invite/v2",\
    json=invite_register)
    assert response_invite_register.status_code == 400

def test_already_in_channel(reset, channel, user1, user2):
    # input parameters for channel_invite_v2
    invite_register = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user2['auth_user_id']
    }

    response_invite_register = requests.post(f"{config.url}channel/invite/v2",\
    json=invite_register)
    response_invite_register = requests.post(f"{config.url}channel/invite/v2",\
    json=invite_register)
    assert response_invite_register.status_code == 400

def test_not_valid_user(reset, channel, user1, user2):

    # input parameters for channel_invite_v2
    invite_register = {
        "token": user1['token'],
        "channel_id": channel['channel_id'],
        "u_id": user2['auth_user_id']
    }

    invite_register['token'] = 'INVALID_TOKEN'

    response_invite_register = requests.post(f"{config.url}channel/invite/v2",\
    json=invite_register)
    assert response_invite_register.status_code == 403

def test_not_valid_member(reset, channel, user2, user3):

    # input parameters for channel_invite_v2
    invite_register = {
        "token": user2['token'],
        "channel_id": channel['channel_id'],
        "u_id": user3['auth_user_id']
    }

    response_invite_register = requests.post(f"{config.url}channel/invite/v2",\
    json=invite_register)
    assert response_invite_register.status_code == 403

'''
import pytest

from src.auth import auth_register_v1, auth_login_v1 
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

@pytest.fixture
def reset():
    clear_v1()

def test_valid(reset):

    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']

    email = "fakeemail_812@outlook.edu.au"
    password = "Password2"
    name_first = "Chris"
    name_last = "Zell"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id_2 = result['auth_user_id']

    channel_name = "channel1_"
    is_public = True
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']
    
    channel_invite_v1(auth_user_id, channel_id, auth_user_id_2)

    assert channel_details_v1(auth_user_id, channel_id) == \
    { 
        'name': 'channel1_',   
        'is_public': is_public, 
        'owner_members': [
            {
                'u_id': auth_user_id, 
                'email': 'realemail_812@outlook.edu.au', 
                'name_first': 'John', 
                'name_last': 'Smith',
                'handle_str': 'johnsmith', 
            }
        ], 
        'all_members': [
            {
                'u_id': auth_user_id, 
                'email': 'realemail_812@outlook.edu.au', 
                'name_first': 'John', 
                'name_last': 'Smith',
                'handle_str': 'johnsmith', 
            },
            {
                'u_id': auth_user_id_2, 
                'email': 'fakeemail_812@outlook.edu.au', 
                'name_first': 'Chris', 
                'name_last': 'Zell',
                'handle_str': 'chriszell', 
            }
        ], 

    }

    
def test_invalid_channel(reset):

    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']

    email = "fakeemail_812@outlook.edu.au"
    password = "Password2"
    name_first = "Chris"
    name_last = "Zell"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id_2 = result['auth_user_id']
    
    channel_name = "channel1_"
    is_public = True
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    # Changing the channel id
    channel_id = result['channel_id'] * 20
    
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, channel_id, auth_user_id_2)

def test_invalid_u_id(reset):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']

    email = "fakeemail_812@outlook.edu.au"
    password = "Password2"
    name_first = "Chris"
    name_last = "Zell"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id_2 = result['auth_user_id']
    
    channel_name = "channel1_"
    is_public = True
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    # Changing the channel id
    channel_id = result['channel_id']

    auth_user_id_2 = auth_user_id_2 * 20
    
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, channel_id, auth_user_id_2)

def test_already_in_channel(reset):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']

    email = "fakeemail_812@outlook.edu.au"
    password = "Password2"
    name_first = "Chris"
    name_last = "Zell"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id_2 = result['auth_user_id']
    
    channel_name = "channel1_"
    is_public = True
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    # Changing the channel id
    channel_id = result['channel_id']

    channel_invite_v1(auth_user_id, channel_id, auth_user_id_2)
    
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, channel_id, auth_user_id_2)

def test_not_valid_user(reset):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']

    email = "fakeemail_812@outlook.edu.au"
    password = "Password2"
    name_first = "Chris"
    name_last = "Zell"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id_2 = result['auth_user_id']
    
    channel_name = "channel1_"
    is_public = True
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    # Changing the channel id
    channel_id = result['channel_id']

    auth_user_id = auth_user_id + auth_user_id_2 + 1
    
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user_id, channel_id, auth_user_id_2)

def test_not_valid_member(reset):
    email = "realemail_812@outlook.edu.au"
    password = "Password1"
    name_first = "John"
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']

    email = "fakeemail_812@outlook.edu.au"
    password = "Password2"
    name_first = "Chris"
    name_last = "Zell"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id_2 = result['auth_user_id']

    email = "fakeremail_812@outlook.edu.au"
    password = "Password3"
    name_first = "John"
    name_last = "Fort"
    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 
    # take auth user id from returned dictionary 
    auth_user_id_3 = result['auth_user_id']
    
    channel_name = "channel1_"
    is_public = True
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    # Changing the channel id
    channel_id = result['channel_id']

    with pytest.raises(AccessError):
        channel_invite_v1(auth_user_id_2, channel_id, auth_user_id_3)


'''