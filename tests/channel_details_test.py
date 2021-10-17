import pytest 
import requests 
from src import config

# Clear all data before testing 

@pytest.fixture
def reset(): 
    requests.delete(f"{config.url}clear/v1")

    data_register = {
        "email" : "realemail_812@outlook.edu.au",
        "password" : "Password1",
        "name_first" : "John",
        "name_last" : "Smith",
    }

    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    data_login = { 
        'email': 'realemail_812@outlook.edu.au', 
        'password': 'Password1', 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)

    return (response.json()['token'], response.json()['auth_user_id'])

def test_one_member(reset): 
    email_1 = "realemail_812@outlook.edu.au"
    name_first_1 = "John"
    name_last_1 = "Smith"
    token = reset[0]
    auth_user_id = reset[1] 

    data_create = { 
        'token': token, 
        'name': "channel1",
        'is_public': True, 
    }

    response = requests.post(f"{config.url}channels/create/v2",\
        json=data_create)
    
    channel_id = response.json()['channel_id'] 

    data_details = { 
        'token': token, 
        'channel_id': channel_id, 
    }

    response = requests.get(f"{config.url}channel/details/v2", \
        json=data_details)
    response_details = response.json() 

    assert response_details == \
    {
        'name': data_create['channel_name'], 
        'is_public': data_create['is_public'], 
        'owner_members': [
            {
                'u_id': auth_user_id, 
                'email': email_1, 
                'name_first': name_first_1, 
                'name_last': name_last_1,
                'handle_str': 'johnsmith', 
            }
        ], 
        'all_members': [
            {
                'u_id': auth_user_id, 
                'email': email_1, 
                'name_first': name_first_1, 
                'name_last': name_last_1,
                'handle_str': 'johnsmith', 
            }
        ], 
    }

def test_invalid_channel(reset): 
    token = reset[0] 

    data_create = { 
        'token': token, 
        'name': 'channel1', 
        'is_public': True, 
    }

    response = requests.post(f"{config.url}channels/create/v2",\
        json=data_create)
    
    channel_id = response.json()['channel_id']

    data_details = { 
        'token': token,
        'channel_id': channel_id + 1, 
    }

    response = requests.get(f'{config.url}channel/details/v2', \
        json=data_details)

    assert response.status_code == 400 

def test_non_member(reset): 
    token_1 = reset[0]
    
    # create 2nd user
    email_2 = "realemail_813@outlook.edu.au"
    password_2 = "Password2"
    name_first_2 = "Johne"
    name_last_2 = "Smithe"


    data_register = {
        "email" : email_2,
        "password" : password_2,
        "name_first" : name_first_2,
        "name_last" : name_last_2,
    }

    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    data_login = { 
        'email': email_2, 
        'password': password_2, 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)
    token_2 = response.json()['token']

    # 1st user creates channel, 2nd user not part of it 
    data_create = { 
        'token': token_1, 
        'name': 'channel1', 
        'is_public': True, 
    }
    
    response = requests.post(f'{config.url}channels/create/v2', json=data_create)
    channel_id = response.json()['channel_id']
    
    # 2nd user tries to call channel details of channel created by 1st user 
    data_details = { 
        'token': token_2, 
        'channel_id': channel_id, 
    }
    response = requests.get(f'{config.url}channel/details/v2', json=data_details)

    assert response.status_code == 403 


def test_invalid_user(reset): 

    data_create = { 
        'token': reset[0], 
        'name': 'channel1', 
        'is_public': True, 
    }

    response = requests.post(f'{config.url}channels/create/v2', json=data_create)
    channel_id = response.json()['channel_id']

    data_details = { 
        'token': '', 
        'channel_id': channel_id, 
    }

    response = requests.get(f'{config.url}channel/details/v2', json=data_details)

    assert response.status_code == 403 

''' REQUIRE CHANNEL JOIN 
def test_two_members(reset): 
    email_1 = "realemail_812@outlook.edu.au"
    name_first_1 = "John"
    name_last_1 = "Smith"

    token_1 = reset[0]
    auth_user_id_1 = reset[1]
    
    email_2 = "realemail_813@outlook.edu.au"
    password_2 = "Password2"
    name_first_2 = "Johne"
    name_last_2 = "Smithe"
    
    data_register = {
        "email" : email_2,
        "password" : password_2,
        "name_first" : name_first_2,
        "name_last" : name_last_2,
    }

    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    data_login = { 
        'email': email_2, 
        'password': password_2, 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)
    auth_user_id_2 = response.json()['auth_user_id']
    token_2 = response.json()['token']

    data_create = { 
        'token': token_1, 
        'name': 'channel1', 
        'is_public': True, 
    }
    channel_name = "channel1"
    is_public = True 
    
    response = requests.post(f'{config.url}channels/create/v2', json=data_create)
    channel_id = response.json()['channel_id']

    data_join = { 
        'token': token_2, 
        'channel_id': channel_id, 
    }
    requests.post(f'{config.url}channel/join/v2', json=data_join)

    data_details = { 
        'token': token_2, 
        'channel_id': channel_id, 
    }

    response = requests.get(f'{config.url}channel/details/v2', json=data_details)
    return_dict = response.json() 

    # check channel name and public / private status is correct 
    assert return_dict['name'] == channel_name 
    assert return_dict['is_public'] == is_public 

    # only 1 owner in this iteration, so checking for only one owner
    assert return_dict['owner_members'] ==  [
        {
            'u_id': auth_user_id_1, 
            'email': email_1, 
            'name_first': name_first_1, 
            'name_last': name_last_1,
            'handle_str': 'johnsmith', 
        }
    ]
    # check owner and members list is correct, returned list can be in any order 
    mem_list = [ 
        {
            'u_id': auth_user_id_1, 
            'email': email_1, 
            'name_first': name_first_1, 
            'name_last': name_last_1, 
            'handle_str': 'johnsmith', 
        }, 
        { 
            'u_id': auth_user_id_2, 
            'email': email_2, 
            'name_first': name_first_2, 
            'name_last': name_last_2, 
            'handle_str': 'johnesmithe', 
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
    name_first_1 = "John"
    name_last_1 = "Smith"

    auth_user_id_1 = reset[1]
    token_1 = reset[0]

    
    email_2 = "realemail_813@outlook.edu.au"
    password_2 = "Password2"
    name_first_2 = "Johne"
    name_last_2 = "Smithe"
    
    data_register = {
        "email" : email_2,
        "password" : password_2,
        "name_first" : name_first_2,
        "name_last" : name_last_2,
    }

    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    data_login = { 
        'email': email_2, 
        'password': password_2, 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)
    auth_user_id_2 = response.json()['auth_user_id']
    token_2 = response.json()['token']


    email_3 = "realemail_814@outlook.edu.au"
    password_3 = "Password3"
    name_first_3 = "Johnny"
    name_last_3 = "Smithy"
    
    data_register = {
        "email" : email_3,
        "password" : password_3,
        "name_first" : name_first_3,
        "name_last" : name_last_3,
    }

    requests.post(
        f"{config.url}auth/register/v2",
        json=data_register
    )

    data_login = { 
        'email': email_3, 
        'password': password_3, 
    }
    
    response = requests.post(f'{config.url}auth/login/v2', json=data_login)
    auth_user_id_3 = response.json()['auth_user_id']
    token_3 = response.json()['token']


    channel_name = "channel1"
    is_public = True 

    data_create = { 
        'token': token_1, 
        'name': channel_name, 
        'is_public': is_public, 
    }

    response = requests.post(f'{config.url}channels/create/v2', json=data_create)
    channel_id = response.json()['channel_id']

    data_join = { 
        'token': token_2, 
        'channel_id': channel_id, 
    }
    requests.post(f'{config.url}channel/join/v2', json=data_join)

    data_join = { 
        'token': token_3, 
        'channel_id': channel_id, 
    }
    requests.post(f'{config.url}channel/join/v2', json=data_join)

    data_details = { 
        'token': token_3, 
        'channel_id': channel_id, 
    }

    response = requests.get(f'{config.url}channel/details/v2', json=data_details)

    return_dict = response.json() 

    assert return_dict['name'] == channel_name 
    assert return_dict['is_public'] == is_public 

    assert return_dict['owner_members'] ==  [
        {
            'u_id': auth_user_id_1, 
            'email': email_1, 
            'name_first': name_first_1, 
            'name_last': name_last_1,
            'handle_str': 'johnsmith', 
        }
    ]

    mem_list = [ 
        {
            'u_id': auth_user_id_1, 
            'email': email_1, 
            'name_first': name_first_1, 
            'name_last': name_last_1, 
            'handle_str': 'johnsmith', 
        }, 
        { 
            'u_id': auth_user_id_2, 
            'email': email_2, 
            'name_first': name_first_2, 
            'name_last': name_last_2, 
            'handle_str': 'johnesmithe', 
        }, 
        { 
            'u_id': auth_user_id_3, 
            'email': email_3, 
            'name_first': name_first_3, 
            'name_last': name_last_3, 
            'handle_str': 'johnnysmithy', 
        }, 
    ]

    new_return_list = sorted(return_dict['all_members'], key = lambda k: k['u_id']) 
    new_mem_list = sorted(mem_list, key = lambda k: k['u_id']) 

    assert new_return_list == new_mem_list 
''' 