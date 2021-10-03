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

    channel_data = channel_details_v1(auth_user_id, channel_id)
    members_list = channel_data['all_members']

    member_in_channel = False
    for members in members_list:
        if members['u_id'] == auth_user_id_2:
            member_in_channel = True

    assert member_in_channel == True
        

    
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

    auth_user_id = auth_user_id * 20
    
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


