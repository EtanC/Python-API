import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1, channel_details_v1
from src.other import clear_v1
from src import config

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

#AUTH
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
        Returns {'auth_user_id': user_id} on successful login
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
        Returns {'auth_user_id': user_id} on successful register
    '''
    data = request.get_json()
    user_id = auth_register_v1(
        data['email'],
        data['password'],
        data['name_first'],
        data['name_last']
    )
    return dumps(user_id)

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



#channel/join/v2
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
                    - User not authorised 

    Return Value: 
        Returns {name, is_public, owner_members, all_members} on successful creation 
    '''

    data = request.get_json() 

    return_dict = channel_details_v1(data['token'], data['channel_id'])
    return dumps(return_dict) 



#MESSAGE
@APP.route("/message/send/v1", methods=['POST'])
def message_send_v1():

    data = request.get_json()
    message = message_send_v1(
        data['token'],
        data['channel_id'],
        data['message']
    )
    return dumps(message)

@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit_v1():
    pass

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove_v1():
    pass

@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm_v1():
    pass








#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
