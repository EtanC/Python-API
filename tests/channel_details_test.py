import pytest 

from src.channels import channels_create_v1 
from src.auth import auth_register_v1, auth_login_v1
from src.other import clear_v1 
from src.error import InputError
from src.error import AccessError 
from src.channel import channel_details_v1 
from src.channel import channel_join_v1 


# Clear all data before testing 
@pytest.fixture
def reset(): 
    clear_v1()
# ----------------------------------------------------------------------------------
# NOTE: COULD USE .str.lower() TO TURN FIRST AND LAST NAME TO LOWERCASE
# AND THE DO handle = first + last STRING ADDITION TO GENERATE HANDLE FOR DIFF NAMES
# ----------------------------------------------------------------------------------
def test_one_member(reset): 
    email_1 = "realemail_812@outlook.edu.au"
    password_1 = "Password1"
    name_first_1 = "John"
    name_last_1 = "Smith"
    auth_register_v1(email_1, password_1, name_first_1, name_last_1)
    result = auth_login_v1(email_1, password_1) 
    # take auth user id from returned dictionary 
    auth_user_id = result['auth_user_id']

    channel_name = "channel1"
    is_public = True 
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']

    assert channel_details_v1(auth_user_id, channel_id) == \
    {
        'name': channel_name, 
        'is_public': is_public, 
        'owner_members': [
            {
                'u_id': auth_user_id, 
                'email': email_1, 
                'name_first': name_first_1, 
                'name_last': name_last_1,
                'handle': 'johnsmith', 
            }
        ], 
        'all_members': [
            {
                'u_id': auth_user_id, 
                'email': email_1, 
                'name_first': name_first_1, 
                'name_last': name_last_1,
                'handle': 'johnsmith', 
            }
        ], 
    }

def test_invalid_channel(reset): 
    email_1 = "realemail_812@outlook.edu.au"
    password_1 = "Password1"
    name_first_1 = "John"
    name_last_1 = "Smith"
    auth_register_v1(email_1, password_1, name_first_1, name_last_1)
    result = auth_login_v1(email_1, password_1) 

    auth_user_id = result['auth_user_id']
    
    channel_name = "channel1"
    is_public = True 
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']

    with pytest.raises(InputError): 
        channel_details_v1(auth_user_id, channel_id + 1)

def test_non_member(reset): 
    email_1 = "realemail_812@outlook.edu.au"
    password_1 = "Password1"
    name_first_1 = "John"
    name_last_1 = "Smith"
    auth_register_v1(email_1, password_1, name_first_1, name_last_1)
    result = auth_login_v1(email_1, password_1) 

    auth_user_id = result['auth_user_id']
    
    email_2 = "realemail_813@outlook.edu.au"
    password_2 = "Password2"
    name_first_2 = "Johne"
    name_last_2 = "Smithe"
    auth_register_v1(email_2, password_2, name_first_2, name_last_2)
    result = auth_login_v1(email_2, password_2) 

    auth_user_id_2 = result['auth_user_id']

    channel_name = "channel1"
    is_public = True 
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']

    with pytest.raises(AccessError): 
        channel_details_v1(auth_user_id_2, channel_id)


def test_invalid_user(reset): 
    email_1 = "realemail_812@outlook.edu.au"
    password_1 = "Password1"
    name_first_1 = "John"
    name_last_1 = "Smith"
    auth_register_v1(email_1, password_1, name_first_1, name_last_1)
    result = auth_login_v1(email_1, password_1) 

    auth_user_id = result['auth_user_id']

    channel_name = "channel1"
    is_public = True 
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']

    with pytest.raises(AccessError): 
        channel_details_v1(auth_user_id + 1, channel_id)

def test_two_members(reset): 
    email_1 = "realemail_812@outlook.edu.au"
    password_1 = "Password1"
    name_first_1 = "John"
    name_last_1 = "Smith"
    auth_register_v1(email_1, password_1, name_first_1, name_last_1)
    result = auth_login_v1(email_1, password_1) 

    auth_user_id = result['auth_user_id']
    
    email_2 = "realemail_813@outlook.edu.au"
    password_2 = "Password2"
    name_first_2 = "Johne"
    name_last_2 = "Smithe"
    auth_register_v1(email_2, password_2, name_first_2, name_last_2)
    result = auth_login_v1(email_2, password_2) 

    auth_user_id_2 = result['auth_user_id']


    channel_name = "channel1"
    is_public = True 
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']

    channel_join_v1(auth_user_id_2, channel_id)

    return_dict = channel_details_v1(auth_user_id_2, channel_id)

    # check channel name and public / private status is correct 
    assert return_dict['name'] == channel_name 
    assert return_dict['is_public'] == is_public 

    # only 1 owner in this iteration, so checking for only one owner
    assert return_dict['owner_members'] ==  [
        {
            'u_id': auth_user_id, 
            'email': email_1, 
            'name_first': name_first_1, 
            'name_last': name_last_1,
            'handle': 'johnsmith', 
        }
    ]
    # check owner and members list is correct, returned list can be in any order 
    mem_list = [ 
        {
            'u_id': auth_user_id, 
            'email': email_1, 
            'name_first': name_first_1, 
            'name_last': name_last_1, 
            'handle': 'johnsmith', 
        }, 
        { 
            'u_id': auth_user_id_2, 
            'email': email_2, 
            'name_first': name_first_2, 
            'name_last': name_last_2, 
            'handle': 'johnesmithe', 
        },
    ]

    # using sorted and lambda function to sort both lists according to u_id
    # this should make it so that both lists are sorted in the same order 
    # and thus allowing for direct comparison 
    new_return_list = sorted(return_dict['all_members'], key = lambda k: k['u_id']) 
    new_mem_list = sorted(mem_list, key = lambda k: k['u_id']) 

    assert new_return_list == new_mem_list 

def test_three_members(reset): 
    email_1 = "realemail_812@outlook.edu.au"
    password_1 = "Password1"
    name_first_1 = "John"
    name_last_1 = "Smith"
    auth_register_v1(email_1, password_1, name_first_1, name_last_1)
    result = auth_login_v1(email_1, password_1) 

    auth_user_id = result['auth_user_id']
    
    email_2 = "realemail_813@outlook.edu.au"
    password_2 = "Password2"
    name_first_2 = "Johne"
    name_last_2 = "Smithe"
    auth_register_v1(email_2, password_2, name_first_2, name_last_2)
    result = auth_login_v1(email_2, password_2) 

    auth_user_id_2 = result['auth_user_id']

    email_3 = "realemail_814@outlook.edu.au"
    password_3 = "Password3"
    name_first_3 = "Johnny"
    name_last_3 = "Smithy"
    auth_register_v1(email_3, password_3, name_first_3, name_last_3)
    result = auth_login_v1(email_3, password_3) 

    auth_user_id_3 = result['auth_user_id']

    channel_name = "channel1"
    is_public = True 
    result = channels_create_v1(auth_user_id, channel_name, is_public)
    channel_id = result['channel_id']

    channel_join_v1(auth_user_id_2, channel_id)
    channel_join_v1(auth_user_id_3, channel_id) 

    return_dict = channel_details_v1(auth_user_id_3, channel_id)

    assert return_dict['name'] == channel_name 
    assert return_dict['is_public'] == is_public 

    assert return_dict['owner_members'] ==  [
        {
            'u_id': auth_user_id, 
            'email': email_1, 
            'name_first': name_first_1, 
            'name_last': name_last_1,
            'handle': 'johnsmith', 
        }
    ]

    mem_list = [ 
        {
            'u_id': auth_user_id, 
            'email': email_1, 
            'name_first': name_first_1, 
            'name_last': name_last_1, 
            'handle': 'johnsmith', 
        }, 
        { 
            'u_id': auth_user_id_2, 
            'email': email_2, 
            'name_first': name_first_2, 
            'name_last': name_last_2, 
            'handle': 'johnesmithe', 
        }, 
        { 
            'u_id': auth_user_id_3, 
            'email': email_3, 
            'name_first': name_first_3, 
            'name_last': name_last_3, 
            'handle': 'johnnysmithy', 
        }, 
    ]

    new_return_list = sorted(return_dict['all_members'], key = lambda k: k['u_id']) 
    new_mem_list = sorted(mem_list, key = lambda k: k['u_id']) 

    assert new_return_list == new_mem_list 
