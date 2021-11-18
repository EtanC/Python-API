from src.helper import token_to_user, decode_token, valid_email
from src.error import AccessError, InputError
from src.data_store import data_store
from src.channel import get_user
from src.auth import valid_name 
import requests
from PIL import Image, ImageChops
import os 
from src import config

def users_all_v1(token): 
    '''
    Given a user's token, return a list of all users and their associated details, 
    including: u_id, email, name_first, name_last, handle_str. 
    Don't return if user has been removed, i.e. if email, password are None 
    
    Arguments:
        token (str): token identifying user
        
    Exceptions: 
        AccessError - invalid token 

    Returns: 
        Returns { users } on successful creation 
    '''

    store = data_store.get()

    token_user = token_to_user(token, store)

    if token_user is None: 
        raise AccessError(description='Invalid token')

    # if token is valid, go through every user in the data store and add their 
    # 'associated details' to the users_list in a dictionary, then return the list 
    # in json format 
    users_list = [] 
    for user in store['users']: 
        # check if user has been removed
        if user['email'] is not None and user['password'] is not None: 
            # add to list if user has not been removed 
            users_list.append({
                'u_id': user['u_id'], 
                'email': user['email'], 
                'name_first': user['name_first'], 
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'profile_img_url': user['profile_img_url'],
            })
    
    return {'users': users_list}

def user_profile_v1(token, u_id): 
    '''
    For a valid user, returns information about their u_id, email, first name, 
    last name and handle_str.

    Arguments: 
        token   (str) - token idenfifying user1 (accessing the route) 
        u_id    (int) - user id of the target / user2
    
    Exceptions: 
        InputError  - u_id does not refer to a valid user2 
        AccessError - user1 invalid token 
    
    Return Value: 
        Returns { user } dictionary on successfull call 
    '''

    store = data_store.get() 
    token_user = token_to_user(token, store)
    if token_user is None: 
        raise AccessError(description='Invalid token')

    user_data = get_user(u_id, store)

    if user_data == None: 
        raise InputError(description='Invalid u_id')

    user = { 
        'u_id': user_data['u_id'], 
        'email': user_data['email'], 
        'name_first': user_data['name_first'], 
        'name_last': user_data['name_last'], 
        'handle_str': user_data['handle_str'], 
        'profile_img_url': user_data['profile_img_url'],
    }

    return {'user': user}

def user_profile_sethandle_v1(token, handle_str): 
    '''
    Update the user's handle (display name)

    Arguments: 
        token       (str)       -   token identifying user 
        handle_str  (str)       -   handle user wants to change to 
    
    Exceptions: 
        InputError  - length of handle_str not between 3-20 chars inclusive
                    - handle_str contains non-alphanumeric chars 
                    - handle already used by another user 
        AccessError - invalid token 
    
    Return Value: 
        Returns {} on successful call 
    '''
    store = data_store.get()

    # token to user returns None if token is invalid 
    token_user = token_to_user(token, store)
    if token_user is None: 
        raise AccessError(description='Invalid token')
    
    if (len(handle_str) < 3) or (len(handle_str) > 20): 
        raise InputError(description='Handle must contain 3-20 characters')
    
    if handle_str.isalnum() == False: 
        raise InputError(description='Handle must be alphanumeric')
    
    for user in store['users']: 
        if handle_str == user['handle_str']: 
            raise InputError(description='Handle already in use')

    # by this point, handle should be within char range, alphanumeric, not used by
    # anyone else and token should be valid, so store the new handle 
    token_user['handle_str'] = handle_str 
    data_store.set(store)

    return {} 

def user_profile_setname_v1(token, name_first, name_last): 
    '''
    Update the authorised user's first and last name

    Arguments: 
        token       (str) - token identifying the user 
        name_first  (str) - first name to change to if valid
        name_last   (str) - last name to change to if valid
    
    Exceptions: 
        InputError  - length of name_first not between 1 and 50 chars inclusive
                    - length of name_last not between 1 and 50 chars inclusive
        AccessError - invalid token 
    
    Return Value: 
        Returns {} on successful call 
    '''
    store = data_store.get() 
    user = token_to_user(token, store)

    if user is None: 
        raise AccessError(description='Invalid token')

    if valid_name(name_first) == False: 
        raise InputError(description='First name must contain 1-50 characters')
    
    if valid_name(name_last) == False: 
        raise InputError(description='Last name must contain 1-50 characters')
    
    # by this point, both the first and last name should be within character range
    # so we just save them into the data_store 
    user['name_first'] = name_first
    user['name_last'] = name_last
    data_store.set(store)

    return {}  

def user_profile_setemail_v1(token, email): 
    '''
    Update the authorised user's email address 

    Arguments: 
        token (str) - token identifying user 
        email (str) - email user wants to change to if valid
    
    Exceptions: 
        InpurError  - Email entered is not in valid format 
                    - Email already used by someone else 
        AccessError - Invalid token
    
    Return Value: 
        Returns {} on successful call 
    '''
    store = data_store.get() 

    user = token_to_user(token, store)

    if user is None: 
        raise AccessError(description='Invalid token')

    # valid email will raise InputError if email is already in use 
    # return True / False based on whether email follows valid format or not 
    if valid_email(email, store) == False: 
        raise InputError(description='Invalid email format')
    
    # by this point email follows valid format and is not used by anyone else
    # so save it 
    user['email'] = email 
    data_store.set(store)

    return {}  


def users_stats_v1(token):
    store = data_store.get()
    user = token_to_user(token, store)
    # Check token
    if user is None:
        raise AccessError(description='Invalid token')

    channels_exist = store['workspace_stats']['channels_exist']
    dms_exist = store['workspace_stats']['dms_exist']
    messages_exist = store['workspace_stats']['messages_exist']

    # Calculate involvement_rate
    active_user_ids = set()
    for channel in store['channels']:
        for user in channel['all_members']:
            active_user_ids.add(user['u_id'])
    for dm in store['dms']:
        for user in dm['members']:
            active_user_ids.add(user['u_id'])
    active_users = len(active_user_ids)

    involvement_rate = active_users / len(store['users'])

    workspace_stats={
        'channels_exist' : channels_exist,
        'dms_exist' : dms_exist,
        'messages_exist' : messages_exist,
        'utilization_rate' : involvement_rate,
    }
    return {'workspace_stats': workspace_stats}

def user_stats_v1(token):
    store = data_store.get()
    user = token_to_user(token, store)
    if user is None:
        raise AccessError(description='Invalid token')
    num_channels_joined = user['channels_joined'][-1]['num_channels_joined']
    num_dms_joined = user['dms_joined'][-1]['num_dms_joined']
    num_msgs_sent = user['messages_sent'][-1]['num_messages_sent']
    num_channels = len(store['channels'])
    num_dms = len(store['dms'])
    num_msgs = store['message_id'] - 1
    if num_channels + num_dms + num_msgs != 0:
        involvement_rate = (num_channels_joined + num_dms_joined +
                            num_msgs_sent) / (num_channels + num_dms + num_msgs)
    else:
        involvement_rate = 0

    if involvement_rate > 1:
        involvement_rate = 1

    stats = {
        'channels_joined' : user['channels_joined'],
        'dms_joined' : user['dms_joined'],
        'messages_sent' : user['messages_sent'],
        'involvement_rate' : involvement_rate,
    }
    return {'user_stats': stats}

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end): 
    '''
    Given a URL of an image on the internet, 
    crops the image within bounds (x_start, y_start) and (x_end, y_end).
    
    Arguments: 
        token   (str)   - token identifying user 
        img_url (str)   - url of image, should only be http not https
        x_start (int)   - left position of crop 
        y_start (int)   - top position of crop 
        x_end   (int)   - right position of crop 
        y_end   (int)   - bottom position of crop 
    
    Exceptions: 
        InputError  - img_url returns HTTP status other than 200 
                    - crop x, y not within boundary
                    - x_end < x_start, y_end < y_start
                    - image uploaded not JPG / JPEG
        AccessError - invalid token
        
    Return Value: 
        Returns {} on successful call
    '''
    store = data_store.get()
    user = token_to_user(token, store)
    # check token 
    if user is None: 
        raise AccessError(description='Invalid token')
    
    # check end values > start values 
    if x_end < x_start or y_end < y_start: 
        raise InputError(description='End value less than start value')

    # check start value
    if x_start < 0 or y_start < 0: 
        raise InputError(description='Crop values out of bounds')
    
    # check url return value
    url_result = requests.get(img_url, stream=True)
    if url_result.status_code != 200: 
        raise InputError(description='Bad url')
    
    image = Image.open(url_result.raw)
    # check image type
    if image.format not in ('JPG', 'JPEG'): 
        raise InputError(description='Image uploaded not a JPG/JPEG')

    img_width, img_height = image.size
    
    # check end value
    if x_end > img_width or y_end > img_height: 
        raise InputError(description='Crop values out of bounds')
    
    # get path of current directory 
    current_path = os.getcwd()
    
    # create path to new directory to store images
    new_directory_path = os.path.join(current_path, 'images')
    
    # if there doesn't exist a directory for storing images, create one
    if not os.path.exists(new_directory_path):
        os.mkdir(new_directory_path)

    # crop image
    image = image.crop((x_start, y_start, x_end, y_end))
    
    # create path for new image, within storage directory
    # store as .jpg since I think jpg == jpeg, should be fine to store both
    # as jpg. 
    # makes finding them later easier
    # store image names as u_id since its unique for each user and thus
    # will make it easier to find
    
    new_image_name = f"{user['u_id']}.jpg"
    new_image_path = os.path.join(new_directory_path, new_image_name)
    image.save(new_image_path)

    data_store.set(store)
    return {}
