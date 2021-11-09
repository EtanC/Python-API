import pytest 
import requests
from src import config 

@pytest.fixture
def reset(): 
    requests.delete(f"{config.url}clear/v1")

    register_owner = {
        "email": "realemail_812@outlook.edu.au",
        "password": "Password1",
        "name_first": "John",
        "name_last": "Smith",
    }
    response_owner = requests.post(
        f"{config.url}auth/register/v2",
        json=register_owner
    )

    register_person = {
        "email": "realemail_1@outlook.edu.au",
        "password": "Password1",
        "name_first": "Abby",
        "name_last": "Smith",
    }
    response_person = requests.post(
        f"{config.url}auth/register/v2",
        json=register_person
    )
    return (response_owner.json(), response_person.json())

def test_valid(reset): 
    u_id1 = reset[1]['auth_user_id']
    register_2 = { 
        "email": "realemail_2@outlook.edu.au",
        "password": "Password2",
        "name_first": "Beta",
        "name_last": "Smith"
    }

    response = requests.post(f"{config.url}auth/register/v2", json=register_2) 
    u_id2 = response.json()['auth_user_id']
    token2 = response.json()['token']

    register_3 = { 
        "email": "realemail_3@outlook.edu.au",
        "password": "Password3",
        "name_first": "Charlie",
        "name_last": "Smith"
    }

    response = requests.post(f"{config.url}auth/register/v2", json=register_3) 
    u_id3 = response.json()['auth_user_id']

    data_create = { 
        'token': reset[0]['token'], 
        'u_ids': [u_id1, u_id2, u_id3]
    }

    response = requests.post(f"{config.url}dm/create/v1", json=data_create)

    data_details = { 
        'token': token2, 
        'dm_id': response.json()['dm_id'], 
    }

    response = requests.get(f"{config.url}dm/details/v1", params=data_details)
    assert response.json()['name'] == 'abbysmith, betasmith, charliesmith, johnsmith'

    expected_list = [{
        'u_id': u_id2,
        'email': 'realemail_2@outlook.edu.au', 
        'name_first': 'Beta', 
        'name_last': 'Smith', 
        'handle_str': 'betasmith',
    }, {
        'u_id': u_id1,
        'email': 'realemail_1@outlook.edu.au', 
        'name_first': 'Abby', 
        'name_last': 'Smith', 
        'handle_str': 'abbysmith',
    }, {
        'u_id': u_id3,
        'email': 'realemail_3@outlook.edu.au', 
        'name_first': 'Charlie', 
        'name_last': 'Smith', 
        'handle_str': 'charliesmith',
    }, {
        'u_id': reset[0]['auth_user_id'], 
        "email": "realemail_812@outlook.edu.au",
        "name_first": "John",
        "name_last": "Smith",
        'handle_str': 'johnsmith',
    }]

    returned_list = response.json()['members']

    sorted_exp_list = sorted(expected_list, key = lambda k: k['u_id']) 
    sorted_ret_list = sorted(returned_list, key = lambda k: k['u_id']) 

    assert sorted_ret_list == sorted_exp_list

def test_more_valid(reset): 
    u_id1 = reset[1]['auth_user_id']
    register_2 = { 
        "email": "realemail_2@outlook.edu.au",
        "password": "Password2",
        "name_first": "Beta",
        "name_last": "Smith"
    }

    response = requests.post(f"{config.url}auth/register/v2", json=register_2) 
    u_id2 = response.json()['auth_user_id']
    token2 = response.json()['token']

    register_3 = { 
        "email": "realemail_3@outlook.edu.au",
        "password": "Password3",
        "name_first": "Charlie",
        "name_last": "Smith"
    }

    response = requests.post(f"{config.url}auth/register/v2", json=register_3) 
    u_id3 = response.json()['auth_user_id']

    register_4 = { 
        "email": "realemail_4@outlook.edu.au",
        "password": "Password4",
        "name_first": "Delta",
        "name_last": "Smith"
    }

    response = requests.post(f"{config.url}auth/register/v2", json=register_4) 
    u_id4 = response.json()['auth_user_id']

    register_5 = { 
        "email": "realemail_5@outlook.edu.au",
        "password": "Password5",
        "name_first": "Evan",
        "name_last": "Smith"
    }

    response = requests.post(f"{config.url}auth/register/v2", json=register_5) 
    u_id5 = response.json()['auth_user_id']

    data_create = { 
        'token': reset[0]['token'], 
        'u_ids': [u_id1, u_id2, u_id3, u_id4, u_id5]
    }

    response = requests.post(f"{config.url}dm/create/v1", json=data_create)

    data_details = { 
        'token': token2, 
        'dm_id': response.json()['dm_id'], 
    }

    response = requests.get(f"{config.url}dm/details/v1", params=data_details)
    assert response.json()['name'] == 'abbysmith, betasmith, charliesmith, deltasmith, evansmith'\
        + ', johnsmith'

    expected_list = [{
        'u_id': u_id2,
        'email': 'realemail_2@outlook.edu.au', 
        'name_first': 'Beta', 
        'name_last': 'Smith', 
        'handle_str': 'betasmith',
    }, {
        'u_id': u_id1,
        'email': 'realemail_1@outlook.edu.au', 
        'name_first': 'Abby', 
        'name_last': 'Smith', 
        'handle_str': 'abbysmith',
    }, {
        'u_id': u_id3,
        'email': 'realemail_3@outlook.edu.au', 
        'name_first': 'Charlie', 
        'name_last': 'Smith', 
        'handle_str': 'charliesmith',
    }, {
        'u_id': u_id5,
        'email': 'realemail_5@outlook.edu.au', 
        'name_first': 'Evan', 
        'name_last': 'Smith', 
        'handle_str': 'evansmith',
    }, {
        'u_id': u_id4,
        'email': 'realemail_4@outlook.edu.au', 
        'name_first': 'Delta', 
        'name_last': 'Smith', 
        'handle_str': 'deltasmith',
    }, {
        'u_id': reset[0]['auth_user_id'], 
        "email": "realemail_812@outlook.edu.au",
        "name_first": "John",
        "name_last": "Smith",
        'handle_str': 'johnsmith',
    }]

    returned_list = response.json()['members']

    sorted_exp_list = sorted(expected_list, key = lambda k: k['u_id']) 
    sorted_ret_list = sorted(returned_list, key = lambda k: k['u_id']) 

    assert sorted_ret_list == sorted_exp_list

def test_invalid_token(reset): 
    u_id1 = reset[1]['auth_user_id']
    register_2 = { 
        "email": "realemail_2@outlook.edu.au",
        "password": "Password2",
        "name_first": "Beta",
        "name_last": "Smith"
    }

    response = requests.post(f"{config.url}auth/register/v2", json=register_2) 
    u_id2 = response.json()['auth_user_id']

    data_create = { 
        'token': reset[0]['token'], 
        'u_ids': [u_id1, u_id2]
    }

    response = requests.post(f"{config.url}dm/create/v1", json=data_create)
    dm_id = response.json()['dm_id']
    data_details = { 
        'token': 'invalid_token', 
        'dm_id': dm_id, 
    }

    response = requests.get(f"{config.url}dm/details/v1", params=data_details)

    assert response.status_code == 403 

def test_invalid_dm_id(reset): 
    u_id1 = reset[1]['auth_user_id']
    register_2 = { 
        "email": "realemail_2@outlook.edu.au",
        "password": "Password2",
        "name_first": "Beta",
        "name_last": "Smith"
    }

    response = requests.post(f"{config.url}auth/register/v2", json=register_2) 
    u_id2 = response.json()['auth_user_id']
    token2 = response.json()['token']

    data_create = { 
        'token': reset[0]['token'], 
        'u_ids': [u_id1, u_id2]
    }

    response = requests.post(f"{config.url}dm/create/v1", json=data_create)
    dm_id = response.json()['dm_id']
    data_details = { 
        'token': token2, 
        'dm_id': dm_id + 1, 
    }

    response = requests.get(f"{config.url}dm/details/v1", params=data_details)
    assert response.status_code == 400 

def test_invalid_member(reset): 
    u_id1 = reset[1]['auth_user_id']
    register_2 = { 
        "email": "realemail_2@outlook.edu.au",
        "password": "Password2",
        "name_first": "Beta",
        "name_last": "Smith"
    }

    response = requests.post(f"{config.url}auth/register/v2", json=register_2) 
    u_id2 = response.json()['auth_user_id']

    data_create = { 
        'token': reset[0]['token'], 
        'u_ids': [u_id1, u_id2]
    }

    response = requests.post(f"{config.url}dm/create/v1", json=data_create)
    dm_id = response.json()['dm_id']

    data_details = { 
        'token': 'INVALID TOKEN', 
        'dm_id': dm_id, 
    }

    response = requests.get(f"{config.url}dm/details/v1", params=data_details)
    assert response.status_code == 403 
