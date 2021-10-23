import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError, AccessError 
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src import config
from src.user import users_all_v1, user_profile_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.user import users_all_v1, user_profile_v1, user_profile_setemail_v1, \
    user_profile_setname_v1, user_profile_sethandle_v1
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.dm import dm_create_v1, dm_list_v1, dm_details_v1
from src.channel import channel_details_v1, channel_messages_v1, channel_join_v1


def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


'''

Auth.py section 

'''


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_v2():
    '''
    Logs the user in after authenticating their identity

    Arguments:
        email    (str)      - The email belonging to the user logging in
        password (str)      - The password corresponding to the email

    Exceptions:
        InputError  - Occurs when email does not belong to a user
                    - Occurs when password is not correct

    Return Value:
        Returns {'token' : token, 'auth_user_id': user_id} on successful call
    '''
    data = request.get_json()
    user_id = auth_login_v1(data['email'], data['password'])
    return dumps(user_id)

@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_v2():
    '''
    Registers the user into Streams when provided with valid details

    Arguments:
        email       (str)      - The user's email, must not be already in use
        password    (str)      - The password chosen by the user
        name_first  (str)      - The first name of the user
        name_last   (str)      - The last name of the user

    Exceptions:
        InputError  - Occurs when email is not a valid email
                    - Occurs when email is already being used by another user
                    - Occurs when password is less than 6 characters
                    - Length of name_first is not between 1 and 50
                    - Length of name_last is not between 1 and 50

    Return Value:
        Returns {'token' : token, 'auth_user_id': user_id} on successful call
    '''
    data = request.get_json()
    user_id = auth_register_v1(
        data['email'],
        data['password'],
        data['name_first'],
        data['name_last']
    )
    return dumps(user_id)


'''

channel.py section 

'''


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    '''
    Returns up to 50 messages from (start), given a channel_id and token

    Arguments:
        token       (str)      - The token used to verify the user's identity
        channel_id  (int)      - The channel's id, used to identify channel
        start       (int)      - The number of the first message to return
                                 eg. The most recent message would be 0
                                     The second most recent message would be 1
                                     And so on

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Start is greater than number of messages in the channel
        AccessError - channel_id is valid and authorised user is not a member
                      of the channel
                    - user_id does not refer to a valid user


    Return Value:
        Returns
        {'messages' : messages, 'start' : start, 'end': end}
        on successful call
    '''
    data = request.args
    messages = channel_messages_v1(
        data['token'],
        int(data['channel_id']),
        int(data['start'])
    )
    return dumps(messages)


@APP.route("/channel/join/v2", methods = ['POST'])
def channel_join_v2():
    '''
        Given a channel_id of a channel that the authorised user can join, 
        adds them to that channel.
        Arguments:

            token (str): token identifying user 
            channel_id (int): id of channel 

        Exceptions: 

            InputError  - Invalid channel id
                        - User already in channel

            AccessError - User is not a member and owner of a private channel

        Returns: 
            Returns {} on successful creation 
    '''
    data = request.get_json() 

    token = data['token'] 
    channel_id = data['channel_id'] 

    empty_dict = channel_join_v1(token, channel_id)
    return dumps(empty_dict)


@APP.route("/channel/details/v2", methods=['GET'])
def channel_details_v2(): 
    '''
    Given a channel with ID channel_id that the authorised user is a member of, 
    provide basic details about the channel 

    Arguments:
        token       (str) - token identifying user
        channel_id  (int) - id of channel 
        
    Exceptions: 
        InputError  - Channel_id not valid 
        AccessError - Authorised user not member of existing channel 
                    - Invalid token 

    Return Value: 
        Returns {name, is_public, owner_members, all_members} on successful creation 
    '''

    data = request.args

    return_dict = channel_details_v1(data['token'], int(data['channel_id']))
    return dumps(return_dict) 



'''

channels.py section 

'''


@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2(): 
    '''
    Creates a channel with the given name, channel can me public or private. 
    Creator of channel is immediately added to the channel. 

    Arguments:
        token       (str)     - token identifying user 
        name        (str)     - name of channel 
        is_public   (bool)    - whether channel is public (True) or private (False)
    
    Exceptions: 
        InputError  - Channel name not between 1 and 20 characters 
        AccessError - Invalid token 

    Return Value: 
        Returns {channel_id} on successful creation 
    '''

    data = request.get_json() 

    channel_id = channels_create_v1(data['token'], data['name'], data['is_public'])

    return dumps(channel_id)

@APP.route("/channels/list/v2", methods=['GET'])
def channels_list_v2(): 
    '''
    Arguments:
        token       (str)     - token identifying user 

    Exceptions: 
        AccessError - User not authorised 

    Return Value: 
        Returns {channels} on successful creation 
    '''

    data = request.args

    channels = channels_list_v1(data['token'])

    return dumps(channels)


@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall_v2(): 
    '''
    Arguments:
        token       (str)     - token identifying user 

    Exceptions: 
        InputError  - Channel_id not valid 
        AccessError - Authorised user not member of existing channel 
                    - Invalid token 

    Return Value: 
        Returns {channels} on successful creation 
    '''
    data = request.args 

    channels = channels_listall_v1(data['token'])

    return dumps(channels)

'''

dms.py section 

'''

@APP.route("/dm/create/v1", methods=['POST'])
def dm_create_v2(): 
    '''
   u_ids contains the user(s) that this DM is directed to, 
   and will not include the creator. 
   The creator is the owner of the DM. 
   name should be automatically generated based on the users that are in this DM. 
   The name should be an alphabetically-sorted, 
   comma-and-space-separated list of user handles, 
   e.g. 'ahandle1, bhandle2, chandle3'.

    Arguments:
        token (str): token identifying user
        u_ids (list): list of u_id 
        
    Exceptions: 
        InputError  - Invalid u_id in the list of u_ids
        AccessError - Invalid token 
        

    Returns: 
        Returns {dm_id} on successful creation 
    '''

    data = request.get_json() 

    return_dict = dm_create_v1(data['token'], data['u_ids'])
    
    return dumps(return_dict) 

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list_v2(): 
    '''
    Returns the list of DMs that the user is a member of.

    Arguments:
        token (str): token identifying user
        
    Exceptions: 
        AccessError - Invalid token 

    Returns: 
        Returns {dms} on successful creation 
    '''

    data = request.args

    return_dict = dm_list_v1(data['token'])
    
    return dumps(return_dict) 

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details(): 
    '''
    Given a DM with ID dm_id that the authorised user is a member of, 
    provide basic details about the DM. 

    Arguments: 
        token (str) - token of a member of the dm
        dm_id (int) - id of the dm 

    Exceptions: 
        InputError  - dm_id does not refer to a valid dm 
        AccessError - authorised user not a member of the dm
                    - user not authorised / invalid token 
                
    Return Value: 
        Returns { name , members } on successful call
    '''

    data = request.args

    return_dict = dm_details_v1(data['token'], int(data['dm_id']))

    return dumps(return_dict)


'''

users.py section 

'''
    
@APP.route("/users/all/v1", methods=['GET'])
def users_all(): 
    '''
    Given a user's token, return a list of all users and their associated details, 
    including: u_id, email, name_first, name_last, handle_str
    
    Arguments:
        token (str) - Token identifying user
        
    Exceptions: 
        AccessError - Invalid token 

    Return Value: 
        Returns { users } on successful call  
    ''' 
    data = request.args

    users = users_all_v1(data['token'])
    return dumps({'users': users}) 

@APP.route("/user/profile/v1", methods=['GET'])
def user_profile(): 
    '''
    For a valid user, returns information about their u_id, email, first name, 
    last name and handle_str.

    Arguments: 
        token   (str) - token identifying user1 (accessing the route) 
        u_id    (int) - user id of the target / user2
    
    Exceptions: 
        InputError  - u_id does not refer to a valid user2 
        AccessError - user1 invalid token 
    
    Return Value: 
        Returns { user } on successful call
    '''
    data = request.args

    user = user_profile_v1(data['token'], int(data['u_id']))

    return dumps({'user': user})

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    '''
    Resets the internal data of the application to its initial state

    Arguments:
        None

    Exceptions:
        None

    Return Value:
        Returns {} on successful call
    '''
    clear_v1()
    return dumps({})

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle(): 
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
    data = request.get_json()
    
    user_profile_sethandle_v1(data['token'], data['handle_str'])

    return dumps({})

@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_profile_setemail(): 
    '''
    Update the authorised user's email address 

    Arguments: 
        token (str) - token identifting user 
        email (str) - email user wants to change to if valid
    
    Exceptions: 
        InpurError  - Email entered is not in valid format 
                    - Email already used by someone else 
        AccessError - Invalid token
    
    Return Value: 
        Returns {} on successful call  
    '''

    data = request.get_json()

    user_profile_setemail_v1(data['token'], data['email'])

    return dumps({})

@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_profile_setname(): 
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

    data = request.get_json() 

    user_profile_setname_v1(data['token'], data['name_first'], data['name_last'])

    return dumps({})

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
