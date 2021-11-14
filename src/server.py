import sys
import signal
from json import dumps
from flask import Flask, request, send_file
from flask_cors import CORS
from src.error import InputError, AccessError 
from src.auth import auth_login_v1, auth_register_v1, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.other import clear_v1
from src import config
from src.user import users_all_v1, user_profile_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.user import users_all_v1, user_profile_v1, user_profile_setemail_v1, \
    user_profile_setname_v1, user_profile_sethandle_v1, user_stats_v1, user_profile_uploadphoto_v1, users_stats_v1

from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_remove_v1, dm_messages_v1, dm_leave_v1
from src.channel import channel_details_v1, channel_messages_v1, channel_join_v1, channel_addowner_v1, channel_invite_v1, channel_removeowner_v1, channel_leave_v1
from src.message import message_edit_v1, message_send_v1, message_senddm_v1, message_remove_v1, message_sendlaterdm_v1, message_sendlater_v1, message_pin_v1
from src.message_react import message_react_v1, message_unreact_v1
from src.admin import admin_userpermission_change_v1, admin_user_remove_v1
from src.standup import standup_start_v1, standup_active_v1
from src.helper import decode_token 
import os 


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

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    '''
    Given an active token, invalidates the token to log the user out.

    Arguments:
        token       (str) - token identifying user

    Exceptions: 
        AccessError - Invalid token

    Return Value: 
        Returns {} on successful logout
    '''
    data = request.get_json()
    return dumps(auth_logout_v1(data['token']))

@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def auth_passwordreset_request():
    '''
    Given a valid email, sends the email a password reset code to reset the
    user's password. Does not raise an error when email is invalid

    Arguments:
        email       (str) - email that the user used to register

    Exceptions: 
        N/A

    Return Value: 
        Returns {}
    '''
    data = request.get_json()
    return dumps(auth_passwordreset_request_v1(data['email']))

@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def auth_passwordreset_reset():
    '''
    Given a reset code and new password, changes the user's password to
    the new password if reset code and new password are valid

    Arguments:
        reset_code      (str) - reset_code sent by Streams app to user's email
        new_password    (str) - new password specified by user

    Exceptions: 
        InputError  - reset_code is not a valid reset code
                    - new_password less than 6 characters long

    Return Value: 
        Returns {}
    '''
    data = request.get_json()
    return dumps(auth_passwordreset_reset_v1(
        data['reset_code'], data['new_password']
    ))

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

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    '''
    Remove user with user id u_id as an owner of the channel.

    Arguments:
        token       (str) - token identifying user
        channel_id  (int) - id of channel 
        u_id        (int) - id of the user to remove as owner from the channel
        
    Exceptions: 
        InputError  - channel_id does not refer to a valid channel
                    - u_id does not refer to a valid user
                    - u_id refers to a user who is not a member of the channel
                    - u_id refers to a user who is already an owner of the
                      channel
        AccessError - Invalid token
                    - the user removing u_id from channel does not have owner
                      permissions

    Return Value: 
        Returns {} on successfully removing
        the user as an owner from the channel
    '''
    data = request.get_json()
    channel_removeowner_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})

@APP.route("/channel/invite/v2", methods = ['POST'])
def channel_invite_v2():
    '''
    Given a channel_id of a channel that the authorised user is a member of, 
    this authorised user can invite a new user to the channel.

    Arguments:
        token (str): token identifying user 
        channel_id (int): id of channel 
        u_id (int): id of user

    Exceptions: 
        InputError  - Invalid channel id
                    - Invalid u_id
                    - User already in channel
        AccessError - User is not a member of the channel

     Returns: 
        Returns {} on successful creation 
    '''
    data = request.get_json()

    return_dict = channel_invite_v1(data['token'], int(data['channel_id']), int(data['u_id']))
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
        InputError  - Channel_id not valid 
        AccessError - Authorised user not member of existing channel 
                    - Invalid token 

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

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    '''
    Will remove the member from the specified channel

    Arguments:
        token       (str)      - The user's token, used to identify and
                                 validate users
        channel_id  (int)      - The channel's id, used to identify channel

    Exceptions:
        InputError  - channel_id does not refer to a valid channel
        AccessError - channel_id is valid and authorised user is not a member
                      of the channel
                    - user_id does not refer to a valid user

    Return Value:
        Returns {} on successful call
    '''
    data = request.get_json()
    channel_leave_v1(data['token'], data['channel_id'])
    return dumps({})

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    '''
    Make user with user id u_id an owner of the channel.

    Arguments:
        token       (str)   - The token used to verify the user's identity
        channel_id  (int)   - The id number used to identify the channel
        u_id        (int)   - The user id used to identify the user to add
                              as an owner

    Exceptions: 
        InputError  - Channel_id not valid
                    - u_id does not refer to a valid user
                    - u_id is not a member of the channel
                    - u_id is already an owner of the channel
        AccessError - Invalid token
                    - Channel is valid and user specified by token does not
                      have owner permissions

    Return Value: 
        Returns {} on adding owner successfully
    '''
    data = request.get_json()
    channel_addowner_v1(data['token'], data['channel_id'], data['u_id'])
    return dumps({})

'''

message.py section 

'''

@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    '''
    Send a message from the authorised user to the channel specified by channel_id. 
    Note: Each message should have its own unique ID, 
    i.e. no messages should share an ID with another message, 
    even if that other message is in a different channel.

    Arguments:
        token       (str) - token identifying user
        channel_id  (int) - id of channel 
        message     (str) - user's message
        
    Exceptions: 
        InputError  - Channel_id not valid 
                    - Message is too short or too long
        AccessError - Authorised user not member of existing channel 
                    - Invalid token  

    Return Value: 
        Returns { message_id } on successful call  
    ''' 

    data = request.get_json()
    message_id = message_send_v1(
        data['token'],
        data['channel_id'],
        data['message']
    )

    return dumps(message_id)

@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():

    '''
    Given a message, update its text with new text. 
    If the new message is an empty string, the message is deleted.
    
    Arguments:
        token       (str) - token identifying user
        message_id  (int) - id of message
        message     (str) - message
        
    Exceptions: 
        InputError  - message is too long
                    - invalid message_id

        AccessError - Authorised user not member of existing channel 
                    - User has no owner permissions
                    - Invalid token 
    Return Value: 
        Returns {} on successful call  
    '''
    data = request.get_json()
    message = message_edit_v1(
        data['token'],
        data['message_id'],
        data['message']
    )
    return dumps(message)

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():

    '''
    Given a message_id for a message, 
    this message is removed from the channel/DM

    Arguments:
        token       (str) - token identifying user
        message_id  (int) - id of message
        
    Exceptions: 
        InputError  - invalid message_id

        AccessError - Authorised user not member of existing channel 
                    - User has no owner permissions
                    - Invalid token 
    Return Value: 
        Returns {} on successful call  
    '''
    data = request.get_json()
    message = message_remove_v1(
        data['token'],
        data['message_id'],
    )
    return dumps(message)


@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():

    '''
    Send a message from authorised_user to the DM specified by dm_id. 
    Note: Each message should have it's own unique ID, 
    i.e. no messages should share an ID with another message, 
    even if that other message is in a different channel or DM.
    
    Arguments:
        token       (str) - token identifying user
        dm_id       (int) - id of dm
        message     (str) - message
        
    Exceptions: 
        InputError  - message is too long or too short
                    - invalid dm_id

        AccessError - Authorised user not member of dm
                    - Invalid token 
    Return Value: 
        Returns {message_id} on successful call  
    '''

    data = request.get_json()
    message = message_senddm_v1(
        data['token'],
        data['dm_id'],
        data['message']
    )
    return dumps(message)

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    '''
    Send a message from the authorised user to the DM specified by dm_id 
    automatically at a specified time in the future.
    
    Arguments: 
        token       (str)   - token identifying user
        dm_id       (int)   - ID of DM that message will be sent to 
        message     (str)   - message that will be sent
        time_sent   (int)   - unix timestamp of when the message will be sent
    
    Exceptions: 
        InputError  - invalid dm_id
                    - length of message over 1000 char 
                    - time_sent is a time of the past
        AccessError - invalid token
                    - dm_id is valid and authorised user is not a member of the dm
    
    Return Value:
        Returns { message_id } on successful call 
    '''
    data = request.get_json()
    message_id = message_sendlaterdm_v1(
        data['token'],
        data['dm_id'],
        data['message'],
        data['time_sent'],
    )
    return dumps(message_id)

@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    '''
    Send a message from authorised user to channel at a specified time in the 
    future. 

    Arguments: 
        token       (str) - token identifying user
        channel_id  (int) - channel_id of channel that message will be sent to
        message     (str) - message that will be sent
        time_sent   (int) - unix timestamp int of when the message will be sent
    
    Exceptions:
        InputError  - invalid channel_id
                    - length of message over 1000 chars
                    - time_sent is a time in the past
        AccessError - channel_id is valid but authorised user is not a part of it
                    - invalid token
    
    Return Value: 
        Returns { message_id } on successful call 
    '''
    data = request.get_json()
    message_id = message_sendlater_v1(
        data['token'], 
        data['channel_id'], 
        data['message'], 
        data['time_sent'],
    )
    return dumps(message_id)

@APP.route("/message/react/v1", methods=['POST'])
def message_react_v3():
    '''
    Given a message within a channel or DM the authorised user is part of, 
    add a "react" to that particular message.
    
    Arguments:
        token       (str) - token identifying user
        message_id       (int) - id of message
        react_id     (int) - id of react
        
    Exceptions: 
        InputError  - Message_id is invalid
                    - React_id is invalid
                    - Message has already been reacted to

        AccessError
                    - Invalid token 
    Return Value: 
        Returns {} 
    '''

    data = request.get_json()
    return_message = message_react_v1(
        data['token'],
        data['message_id'],
        data['react_id']
    )
    return dumps(return_message)

@APP.route("/message/unreact/v1", methods=['POST'])
def message_uneact_v3():
    '''
    Given a message within a channel or DM the authorised user is part of, 
    remove a "react" to that particular message.
    
    Arguments:
        token       (str) - token identifying user
        message_id       (int) - id of message
        react_id     (int) - id of react
        
    Exceptions: 
        InputError  - Message_id is invalid
                    - React_id is invalid
                    - Message have not been reacted to

        AccessError
                    - Invalid token 
    Return Value: 
        Returns {} 
    '''

    data = request.get_json()
    return_message = message_unreact_v1(
        data['token'],
        data['message_id'],
        data['react_id']
    )
    return dumps(return_message)

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    '''
    Given a message within a channel or DM, mark it as "pinned".
    
    Arguments:
        token       (str) - token identifying user
        message_id  (str) - id of message
        
    Exceptions: 
        InputError  - message is already pinned
                    - invalid message_id

        AccessError - Authorised user not owner
                    - Invalid token 
    Return Value: 
        Returns {} on successful call  
    '''
    data = request.get_json()
    message = message_pin_v1(
        data['token'],
        data['message_id'],
    )
    return dumps(message)


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

    return_dict = dm_create_v1(data['token'], list(data['u_ids']))
    
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

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove_v2(): 
    '''
    Returns the list of DMs that the user is a member of.

    Arguments:
        token (str): token identifying user
        
    Exceptions: 
        AccessError - Invalid token 

    Returns: 
        Returns {} on successful creation 
    '''

    data = request.get_json()

    return_dict = dm_remove_v1(data['token'], int(data['dm_id']))
    
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

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages_v2(): 
    '''
    Given a DM with ID dm_id that the authorised user is a member of, 
    return up to 50 messages between index "start" and "start + 50". 
    Message with index 0 is the most recent message in the DM. 
    This function returns a new index "end" which is the value of "start + 50", 
    or, if this function has returned the least recent messages in the DM, 
    returns -1 in "end" to indicate there are no more messages to load after this return.

    Arguments:
        token (str): token identifying user
        dm_id (int): specific dm_id of a message 
        start (int): message index 
        
    Exceptions: 
        InputError  - Invalid dm_id, 
                    - Start is greater than the totla number of messages in the channel
        AccessError - Invalid token 
        

    Returns: 
        Returns {messages, start, end} on successful creation 
    '''

    data = request.args 

    return_dict = dm_messages_v1(data['token'], int(data['dm_id']), int(data['start']))
    
    return dumps(return_dict) 

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave_v2(): 
    '''
    Given a DM ID, the user is removed as a member of this DM. 
    The creator is allowed to leave and the DM will still exist if this happens. 
    This does not update the name of the DM.

    Arguments:
        token (str): token identifying user
        dm_id (int): specific dm_id of a message 
        
    Exceptions: 
        InputError  - Invalid dm_id, 
        AccessError - Invalid token 
        

    Returns: 
        Returns {} on successful creation 
    '''

    data = request.get_json()

    return_dict = dm_leave_v1(data['token'], int(data['dm_id']))
    
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
    return dumps(users) 

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
    return dumps(user)


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

@APP.route("/users/stats/v1", methods=['GET'])
def users_stats():
    '''
    When given a valid token, retrieves the workspace_stats
    
    Arguments: 
        token       (str) - token identifying the user 

    Exceptions: 
        AccessError - invalid token 
    
    Return Value: 
        Returns {
            channels_exist: [{num_channels_exist, time_stamp}],
            dms_exist: [{num_dms_exist, time_stamp}],
            message_exist: [{num_messages_exist, time_stamp}],
            utilization_rate,
        } on successful call
    '''
    data = request.args
    return dumps(users_stats_v1(data['token']))

@APP.route("/user/stats/v1", methods=['GET'])
def user_stats():
    '''
    Given a token, returns data/statistics about the user's usage of Streams

    Arguments: 
        token       (str) - token identifying the user 
    
    Exceptions: 
        AccessError - invalid token 
    
    Return Value: 
        On successful call, returns dictionary of shape
    {
     channels_joined: [{num_channels_joined, time_stamp}],
     dms_joined: [{num_dms_joined, time_stamp}], 
     messages_sent: [{num_messages_sent, time_stamp}], 
     involvement_rate 
    }
    '''
    data = request.args
    return dumps(user_stats_v1(data['token']))

@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def user_profile_uploadphoto(): 
    data = request.get_json()
    return dumps(user_profile_uploadphoto_v1(data['token'], data['img_url'], \
        data['x_start'], data['y_start'], data['x_end'], data['y_end']))

@APP.route("/user/profile/photo/<user_id>.jpg", methods=['GET'])
def user_showphoto(user_id): 
    # ASSUMING THIS IS ONLY CALLED FOR TESTING, THUS NO NEED FOR ERRORCHECKING
    # ASSUME PHOTO HAS ALREADY BEEN UPLOADED
    return send_file(f'{os.getcwd()}/images/{user_id}.jpg', mimetype='image/jpg')

'''

admin.py section

'''

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_delete():
    '''
    Given a user by their u_id, remove them from the Streams.

    Arguments: 
        token (str) - token of a member of the dm
        u_id (int) - id of user

    Exceptions: 
        InputError  - u_id does not refer to a valid user
                    - u_id refers to a user who is the only global owner
        AccessError - authorised user is not a global owner
                
    Return Value: 
        Returns {} on successful call
    '''

    data = request.get_json()

    return_dict = admin_user_remove_v1(data['token'], int(data['u_id']))

    return dumps(return_dict)

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change():
    '''
    Given a user by their user ID, 
    set their permissions to new permissions described by permission_id.

    Arguments: 
        token (str) - token of a member of the dm
        u_id (int) - id of user
        permission_id (int) - value that determines permissions of user

    Exceptions: 
        InputError  - u_id does not refer to a valid user
                    - u_id refers to a user who is the only global owner
                    - permission_id is invalid
        AccessError - authorised user is not a global owner
                
    Return Value: 
        Returns {} on successful call
    '''

    data = request.get_json()

    return_dict = admin_userpermission_change_v1(data['token'], int(data['u_id']), int(data['permission_id']))

    return dumps(return_dict)

'''

standup.py section

'''

@APP.route("/standup/start/v1", methods=['POST'])
def standup_start():
    '''
    Given a token, channel id and standup length, starts a standup in the given
    channel

    Arguments: 
        token       (str)   - Token of user starting the standup
        channel_id  (int)   - Id of the channel the standup belongs to
        length      (int)   - Length of the standup in seconds

    Exceptions: 
        InputError  - Invalid channel id
                    - Length is negative
                    - Active standup already running in channel
        AccessError - Token is invalid
                    - Channel id is valid and user is not member of channel
    Return Value:
        Returns {time_finish} on successful call
    '''

    data = request.get_json()
    return dumps(
        standup_start_v1(data['token'], data['channel_id'], data['length'])
    )

@APP.route("/standup/active/v1", methods=['GET'])
def standup_active():
    '''
    For a given channel, return whether a standup is active in it, and what time the standup finishes. 
    If no standup is active, then time_finish returns None.

    Arguments: 
        token       (str)   - Token of user starting the standup
        channel_id  (int)   - Id of the channel the standup belongs to

    Exceptions: 
        InputError  - Invalid channel id
        AccessError - Token is invalid
                    - Channel id is valid and user is not member of channel
    Return Value:
        Returns {is_active, time_finish} on successful call
    '''

    data = request.args
    return dumps(
        standup_active_v1(data['token'], int(data['channel_id']))
    )


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

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
