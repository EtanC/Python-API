import pytest

from src.channel import channel_join_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError
from src.auth import auth_register_v1, auth_login_v1 
from src.channels import channels_create_v1

# this runs before every test function.
@pytest.fixture
def reset_data():
    clear_v1()

@pytest.fixture
def create_and_reset():

    # creates a real user before every test after clear_v1.
    clear_v1()

    # creates a real user before every test after clear_v1.
    email = "Jack.jones@gmail.com.au"
    password = "Password1"
    name_first = "Jack"
    name_last = "Jones"

    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 

    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']
    return auth_user_id

def test_invalid_user_error(create_and_reset):

    # Create first user from the fixture
    user_id1 = create_and_reset

    # First user creates a public channel
    is_public = True
    name = 'JohnCena_public'
    channel = channels_create_v1(user_id1 ,name, is_public)
    channel_id = channel['channel_id']

    # Invalid user error
    with pytest.raises(InputError):
        channel_join_v1(user_id1 + 1, channel_id)
        
def test_invalid_channel_error(create_and_reset):

    # Create 1st user from the fixture
    user_id1 = create_and_reset

    # Create 2nd user
    email = "jamessmith@gmail.com"
    password = "asdfgh"
    name_first = "James "
    name_last = "Smih"
    auth_register_v1(email, password, name_first, name_last)
    result2 = auth_login_v1(email, password) 
    user_id2 = result2['auth_user_id']

    # 1st user creates a public channel
    is_public = True
    name = 'JohnCena_public'
    channel = channels_create_v1(user_id1 ,name, is_public)
    channel_id = channel['channel_id']

    # Invalid channel error
    with pytest.raises(InputError):
        channel_join_v1(user_id2, channel_id + 1)  

def test_user_already_in_channel_error(create_and_reset):

    # Create 1st user from the fixture
    user_id1 = create_and_reset

    # 1st user creates a public channel
    is_public = True    
    name1 = 'JohnSmith_public'
    channel1 = channels_create_v1(user_id1 ,name1, is_public)
    channel_id_1 = channel1['channel_id']

    # Create 2nd user
    email = "jamessmith@gmail.com"
    password = "asdfgh"
    name_first = "James "
    name_last = "Smih"
    auth_register_v1(email, password, name_first, name_last)
    result2 = auth_login_v1(email, password) 
    
    # 2nd user creates a public channel
    user_id2 = result2['auth_user_id']
    name2 = 'JamesSmith_public'
    channel2 = channels_create_v1(user_id2, name2, is_public)
    channel_id_2 = channel2['channel_id']

    # Both users already in channel as owners error
    with pytest.raises(InputError):
        channel_join_v1(user_id1, channel_id_1)
        channel_join_v1(user_id2, channel_id_2)

def test_private_channel(create_and_reset):

    # Create 1st user from fixture
    user_id1 = create_and_reset

    # 1st user creates a private channel
    is_public = False
    name = 'JohnCena_public'
    channel = channels_create_v1(user_id1 ,name, is_public)
    channel_id = channel['channel_id']

    # Create 2nd user
    email = "jamessmith@gmail.com"
    password = "asdfgh"
    name_first = "James "
    name_last = "Smih"
    auth_register_v1(email, password, name_first, name_last)
    result2 = auth_login_v1(email, password) 
    user_id2 = result2['auth_user_id']

    # Cannot join private channel error
    with pytest.raises(AccessError):
        channel_join_v1(user_id2, channel_id)

def test_channel_join(create_and_reset):

    # Get 1st user from the fixture
    user_id = create_and_reset

    # 1st user creates a public channel
    is_public = True
    name = 'can_join_public'
    channel = channels_create_v1(user_id ,name, is_public)
    channel_id = channel['channel_id']

    # Create 2nd user which can join the public channel
    email = "jamessmith@gmail.com"
    password = "asdfgh"
    name_first = "James "
    name_last = "Smih"
    auth_register_v1(email, password, name_first, name_last)
    result2 = auth_login_v1(email, password) 
    user_id2 = result2['auth_user_id']

    assert(channel_join_v1(user_id2, channel_id)) == {}

def test_channel_join_multi(create_and_reset):

    # Get 1st user from the fixture 
    user_id = create_and_reset

    # 1st user creates a public channel
    is_public = True
    name = 'can_join_public'
    channel = channels_create_v1(user_id ,name, is_public)
    channel_id = channel['channel_id']

    # Create 2nd user which can join the public channel
    email = "jamessmith@gmail.com"
    password = "asdfgh"
    name_first = "James "
    name_last = "Smih"
    auth_register_v1(email, password, name_first, name_last)
    result2 = auth_login_v1(email, password) 
    user_id2 = result2['auth_user_id']

    # Create 2nd user which can join the public channel
    email = "JackDean@hotmail.com"
    password = "qwedfg"
    name_first = "Jack "
    name_last = "Dean"
    auth_register_v1(email, password, name_first, name_last)
    result3 = auth_login_v1(email, password) 
    user_id3 = result3['auth_user_id']

    assert(channel_join_v1(user_id2, channel_id)) == {}
    assert(channel_join_v1(user_id3, channel_id)) == {}

