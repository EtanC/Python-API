import pytest

from src.auth import auth_register_v1, auth_login_v1 
from src.channels import channels_create_v1
from src.channel import channel_invite_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

@pytest.fixture
def reset():
    clear_v1()

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
    # auth_user_id_2 = result['auth_user_id']
    return auth_user_id

def test_valid(reset):
    auth_user_id = reset

    channel_name = "channel1_"
    is_public = True
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']

    # u_id of the second user that was created
    u_id = "2"
    
    channel_invite_v1(auth_user_id, channel_id, u_id)
    # assert that user is now in channel
    
def test_invalid_channel(reset):
    auth_user_id = reset

    channel_name = "channel1_"
    is_public = True
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    # Changing the channel id
    channel_id = result['channel_id'] * 20

    # u_id of the second user that was created
    u_id = "2"
    
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, channel_id, u_id)

def test_invalid_u_id(reset):
    auth_user_id = reset

    channel_name = "channel1_"
    is_public = True
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    # Changing the channel id
    channel_id = result['channel_id']

    # u_id increments by 1 for every new user, but there are only two
    # so this is an invalid u_id
    u_id = "10"
    
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, channel_id, u_id)

def test_already_in_channel(reset):


def test_not_member(reset):



