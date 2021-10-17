import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1
from src import config
from src.user import users_all_v1

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

@APP.route("/users/all/v1", methods=['GET'])
def users_all(): 
    '''
    Given a user's token, return a list of all users and their associated details, 
    including: u_id, email, name_first, name_last, handle_str
    
    Arguments:
        token (str): token identifying user
        
    Exceptions: 
        AccessError - User not authorised 

    Returns: 
        Returns {users} on successful creation 
    '''

    data = request.get_json() 

    users = users_all_v1(data['token'])

    return dumps({'users': users}) 
#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
