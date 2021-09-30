import pytest

from src.channel import channel_join_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError
from src.auth import auth_register_v1, auth_login_v1 

#channel_join_v1(auth_user_id, channel_id):
#channels_create_v1(auth_user_id, name, is_public):
#auth_register_v1(email, password, name_first, name_last):

#create user 1
@pytest.fixture 
def create_user1():

    clear_v1()
    email = "valid1@gmail.com"
    password = "password1"
    name_first = "John"
    name_last = "Smith"
    result = auth_register_v1(email, password, name_first, name_last)
    auth_user_id = result['auth_user_id']
    return auth_user_id

#create user 2
@pytest.fixture 
def create_user2():

    clear_v1()
    email = "valid2@yahoo.com"
    password = "password2"
    name_first = "Jack"
    name_last = "Smith"
    result = auth_register_v1(email, password, name_first, name_last)
    auth_user_id = result['auth_user_id']
    return auth_user_id

#create public channel
@pytest.fixture 
def create_public_channel():

    clear_v1()
    channel_name = "Channel1"
    is_public = True
    u_id = create_user1()
    public_channel = channels_create_v1(u_id, channel_name is_public)
    channel_id = public_channel['channel_id']

    return channel_id

#create private channel
@pytest.fixture 
def create_private_channel():

    clear_v1()
    channel_name = "Channel2"
    is_public = False
    u_id = create_user2()
    private_channel = channels_create_v1(u_id, channel_name is_public)
    channel_id = private_channel['channel_id']

    return channel_id


#test being able to join a channel as usual
def test_join_public_channel_valid():
    auth_user_id = create_user1()
    channel_id = create_public_channel()
    assert(channel_join_v1(auth_user_id, channel_id))

#if channel is invalid
def test_invalid_channel_id():

    auth_user_id = create_user1()
    channel_id = 0

    with pytest.raises(InputError):
        channels_join_v1(auth_user_id, channel_id)

#if channel is private but the user is not invited
def test_private_channel():

    auth_user_id1 = create_user1()
    channel_id = create_private_channel
    channel_join_v1(auth_user_id1, channel_id)
    auth_user_id2 = create_user2()

    # user1 is invited to priv but not user2
    with pytest.raises(InputError):
        channels_join_v1(auth_user_id2, channel_id)
