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
    email = "Jackjones@gmail.com.au"
    password = "Password1"
    name_first = "Jack"
    name_last = "Jones"

    auth_register_v1(email, password, name_first, name_last)
    result = auth_login_v1(email, password) 

    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']
    return auth_user_id

def test_invalid_user_error(create_and_reset):

    #get user_id from the fixture
    user_id = create_and_reset

    #create a public channel
    is_public = True
    name = 'JohnCena_public'
    channel = channels_create_v1(user_id ,name, is_public)
    channel_id = channel['channel_id']


    with pytest.raises(InputError):
        channel_join_v1(user_id + 1, channel_id)
        #user_id + 1 to a diff user

def test_invalid_channel_error(create_and_reset):

    #get user_id from the fixture
    user_id = create_and_reset

    # Create person 2
    email = "jamessmith@gmail.com"
    password = "asdfgh"
    name_first = "James "
    name_last = "Smih"
    auth_register_v1(email, password, name_first, name_last)
    result2 = auth_login_v1(email, password) 
    user_id2 = result2['auth_user_id']

    #create a public channel
    is_public = True
    name = 'JohnCena_public'
    channel = channels_create_v1(user_id ,name, is_public)
    channel_id = channel['channel_id']


    with pytest.raises(InputError):
        channel_join_v1(user_id2, channel_id + 1)
        #channel_id + 1 to a diff channel

def test_user_already_in_channel_error(create_and_reset):

    #auth_user_id = create_and_reset
    is_public = True

    # person 1
    email = "johnsmith@gmail.com"
    password = "qwerty"
    name_first = "John "
    name_last = "Smith"
    auth_register_v1(email, password, name_first, name_last)
    result1 = auth_login_v1(email, password) 
    
    # person 1 creates a public channel
    user_id1 = result1['auth_user_id']
    name1 = 'JohnSmith_public'
    channel1 = channels_create_v1(user_id1 ,name1, is_public)
    channel_id_1 = channel1['channel_id']

    # person 2
    email = "jamessmith@gmail.com"
    password = "asdfgh"
    name_first = "James "
    name_last = "Smih"
    auth_register_v1(email, password, name_first, name_last)
    result2 = auth_login_v1(email, password) 
    
    # person 2 creates a public channel
    user_id2 = result2['auth_user_id']
    name2 = 'JamesSmith_public'
    channel2 = channels_create_v1(user_id2, name2, is_public)
    channel_id_2 = channel2['channel_id']

    with pytest.raises(InputError):
        channel_join_v1(user_id1, channel_id_1)
        channel_join_v1(user_id2, channel_id_2)

def test_private_channel(create_and_reset):
    user_id = create_and_reset

    #create a private channel
    is_public = False
    name = 'JohnCena_public'
    channel = channels_create_v1(user_id ,name, is_public)
    channel_id = channel['channel_id']


    # Create person 2
    email = "jamessmith@gmail.com"
    password = "asdfgh"
    name_first = "James "
    name_last = "Smih"
    auth_register_v1(email, password, name_first, name_last)
    result2 = auth_login_v1(email, password) 
    user_id2 = result2['auth_user_id']

    with pytest.raises(AccessError):
        channel_join_v1(user_id2, channel_id)