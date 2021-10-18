import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError, AccessError 
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src import config
from src.helper import decode_token 
from src.channels import channels_create_v1
from src.channel import channel_details_v1, channel_messages_v1

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

@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    '''
    Returns up to 50 messages from (start), given a channel_id and user_id

    Arguments:
        user_id     (int)      - The user's id, used to identify users
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
    data = request.get_json()
    messages = channel_messages_v1(
        data['token'],
        data['channel_id'],
        data['start']
    )
    return dumps(messages)

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

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2(): 
    '''
    Creates a channel with the given name, channel can me public or private. 
    Creator of channel is immediately added to the channel. 

    Arguments:
        token (str): token identifying user 
        name (str): name of channel 
        is_public (bool): whether channel is public (True) or private (False)
    
    Exceptions: 
        InputError  - Channel name not between 1 and 20 characters 
        AccessError - User not authorised 

    Returns: 
        Returns {channel_id} on successful creation 
    '''

    data = request.get_json() 

    channel_id = channels_create_v1(data['token'], data['name'], data['is_public'])

    return dumps(channel_id)

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details_v2(): 
    '''
    Given a channel with ID channel_id that the authorised user is a member of, 
    provide basic details about the channel 

    Arguments:
        token (str): token identifying user
        channel_id (int): id of channel 
        
    Exceptions: 
        InputError  - Channel_id not valid 
        AccessError - Authorised user not member of existing channel 
                    - User not authorised 

    Returns: 
        Returns {name, is_public, owner_members, all_members} on successful creation 
    '''

    data = request.get_json() 

    return_dict = channel_details_v1(data['token'], data['channel_id'])
    return dumps(return_dict) 

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
