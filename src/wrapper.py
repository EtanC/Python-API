from werkzeug.exceptions import HTTPException
import pytest
import requests
from src.error import InputError, AccessError
from src import config

def parse_response(response):
    if response.status_code in [200, 201]:
        return response.json()
    elif response.status_code == 400:
        raise InputError()
    elif response.status_code == 403:
        raise AccessError()
    else:
        raise Exception(response)

def clear():
    response = requests.delete(
        f'{config.url}clear/v1',
    )
    return parse_response(response)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                   AUTH                                        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def auth_login(email, password):
    response = requests.post(
        f"{config.url}auth/login/v2",
        json={'email' : email, 'password' : password}
    )
    return parse_response(response)

def auth_register(email, password, name_first, name_last):
    res = requests.post(
        f"{config.url}auth/register/v2",
        json={
            'email' : email,
            'password' : password,
            'name_first' : name_first,
            'name_last' : name_last,
        }
    )
    return parse_response(res)

def auth_logout(token):
    res = requests.post(
        f"{config.url}auth/logout/v1",
        json={
            'token' : token,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                   channels                                    
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def channels_create(token, name, is_public):
    res = requests.post(
        f"{config.url}channels/create/v2",
        json={
            'token' : token,
            'name' : name,
            'is_public' : is_public,
        }
    )
    return parse_response(res)

def channels_list(token):
    res = requests.get(
        f"{config.url}channels/list/v2",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

def channels_listall(token):
    res = requests.get(
        f"{config.url}channels/listall/v2",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                   channel                                     
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def channel_details(token, channel_id):
    res = requests.get(
        f"{config.url}channel/details/v2",
        params={
            'token' : token,
            'channel_id' : channel_id,
        }
    )
    return parse_response(res)

def channel_join(token, channel_id):
    res = requests.post(
        f"{config.url}channel/join/v2",
        json={
            'token' : token,
            'channel_id' : channel_id,
        }
    )
    return parse_response(res)

def channel_invite(token, channel_id, u_id):
    res = requests.post(
        f"{config.url}channel/invite/v2",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'u_id' : u_id,
        }
    )
    return parse_response(res)

def channel_messages(token, channel_id, start):
    res = requests.get(
        f"{config.url}channel/messages/v2",
        params={
            'token' : token,
            'channel_id' : channel_id,
            'start' : start,
        }
    )
    return parse_response(res)

def channel_leave(token, channel_id):
    res = requests.post(
        f"{config.url}channel/leave/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
        }
    )
    return parse_response(res)

def channel_addowner(token, channel_id, u_id):
    res = requests.post(
        f"{config.url}channel/addowner/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'u_id' : u_id,
        }
    )
    return parse_response(res)

def channel_removeowner(token, channel_id, u_id):
    res = requests.post(
        f"{config.url}channel/removeowner/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'u_id' : u_id,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                   message                                     
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def message_send(token, channel_id, message):
    res = requests.post(
        f"{config.url}message/send/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : message,
        }
    )
    return parse_response(res)

def message_edit(token, message_id, message):
    res = requests.put(
        f"{config.url}message/edit/v1",
        json={
            'token' : token,
            'message_id' : message_id,
            'message' : message,
        }
    )
    return parse_response(res)

def message_remove(token, message_id):
    res = requests.delete(
        f"{config.url}message/remove/v1",
        json={
            'token' : token,
            'message_id' : message_id,
        }
    )
    return parse_response(res)

def message_share(token, og_message_id, message, channel_id, dm_id):
    res = requests.post(
        f"{config.url}message/share/v1",
        json={
            'token' : token,
            'og_message_id' : og_message_id,
            'message' : message,
            'channel_id' : channel_id,
            'dm_id' : dm_id,
        }
    )
    return parse_response(res)

def message_react(token, message_id, react_id):
    res = requests.post(
        f"{config.url}message/react/v1",
        json={
            'token' : token,
            'message_id' : message_id,
            'react_id' : react_id,
        }
    )
    return parse_response(res)

def message_unreact(token, message_id, react_id):
    res = requests.post(
        f"{config.url}message/unreact/v1",
        json={
            'token' : token,
            'message_id' : message_id,
            'react_id' : react_id,
        }
    )
    return parse_response(res)

def message_pin(token, message_id):
    res = requests.post(
        f"{config.url}message/pin/v1",
        json={
            'token' : token,
            'message_id' : message_id,
        }
    )
    return parse_response(res)

def message_unpin(token, message_id):
    res = requests.post(
        f"{config.url}message/unpin/v1",
        json={
            'token' : token,
            'message_id' : message_id,
        }
    )
    return parse_response(res)

def message_sendlater(token, channel_id, message, time_sent):
    res = requests.post(
        f"{config.url}message/sendlater/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : message,
            'time_sent' : time_sent,
        }
    )
    return parse_response(res)

def message_sendlaterdm(token, dm_id, message, time_sent):
    res = requests.post(
        f"{config.url}message/sendlaterdm/v1",
        json={
            'token' : token,
            'dm_id' : dm_id,
            'message' : message,
            'time_sent' : time_sent,
        }
    )
    return parse_response(res)

def standup_start(token, channel_id, length):
    res = requests.post(
        f"{config.url}standup/start/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'length' : length,
        }
    )
    return parse_response(res)

def standup_active(token, channel_id):
    res = requests.get(
        f"{config.url}standup/active/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
        }
    )
    return parse_response(res)

def standup_send(token, channel_id, message):
    res = requests.post(
        f"{config.url}standup/send/v1",
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : message,
        }
    )
    return parse_response(res)

def auth_passwordreset_request(email):
    res = requests.post(
        f"{config.url}auth/passwordreset/request/v1",
        json={
            'email' : email,
        }
    )
    return parse_response(res)

def auth_passwordreset_reset(reset_code, new_password):
    res = requests.post(
        f"{config.url}auth/passwordreset/reset/v1",
        json={
            'reset_code' : reset_code,
            'new_password' : new_password,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                      dm                                       
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def dm_create(token, u_ids):
    res = requests.post(
        f"{config.url}dm/create/v1",
        json={
            'token' : token,
            'u_ids' : u_ids,
        }
    )
    return parse_response(res)

def dm_list(token):
    res = requests.get(
        f"{config.url}dm/list/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

def dm_remove(token, dm_id):
    res = requests.delete(
        f"{config.url}dm/remove/v1",
        json={
            'token' : token,
            'dm_id' : dm_id,
        }
    )
    return parse_response(res)

def dm_details(token, dm_id):
    res = requests.get(
        f"{config.url}dm/details/v1",
        params={
            'token' : token,
            'dm_id' : dm_id,
        }
    )
    return parse_response(res)

def dm_leave(token, dm_id):
    res = requests.post(
        f"{config.url}dm/leave/v1",
        json={
            'token' : token,
            'dm_id' : dm_id,
        }
    )
    return parse_response(res)

def dm_messages(token, dm_id, start):
    res = requests.get(
        f"{config.url}dm/messages/v1",
        params={
            'token' : token,
            'dm_id' : dm_id,
            'start' : start,
        }
    )
    return parse_response(res)

def message_senddm(token, dm_id, message):
    res = requests.post(
        f"{config.url}message/senddm/v1",
        json={
            'token' : token,
            'dm_id' : dm_id,
            'message' : message,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                   users                                       
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def users_all(token):
    res = requests.get(
        f"{config.url}users/all/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

def users_stats(token):
    res = requests.get(
        f"{config.url}users/stats/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                    user                                       
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def user_profile(token, u_id):
    res = requests.get(
        f"{config.url}user/profile/v1",
        params={
            'token' : token,
            'u_id' : u_id,
        }
    )
    return parse_response(res)

def user_profile_setname(token, name_first, name_last):
    res = requests.put(
        f"{config.url}user/profile/setname/v1",
        json={
            'token' : token,
            'name_first' : name_first,
            'name_last' : name_last,
        }
    )
    return parse_response(res)

def user_profile_setemail(token, email):
    res = requests.put(
        f"{config.url}user/profile/setemail/v1",
        json={
            'token' : token,
            'email' : email,
        }
    )
    return parse_response(res)

def user_profile_sethandle(token, handle_str):
    res = requests.put(
        f"{config.url}user/profile/sethandle/v1",
        json={
            'token' : token,
            'handle_str' : handle_str,
        }
    )
    return parse_response(res)

def user_stats(token):
    res = requests.get(
        f"{config.url}user/stats/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    res = requests.post(
        f"{config.url}user/profile/uploadphoto/v1",
        json={
            'token' : token, 
            'img_url' : img_url, 
            'x_start' : x_start, 
            'y_start' : y_start, 
            'x_end' : x_end, 
            'y_end' : y_end,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                    admin                                      
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def admin_user_remove(token, u_id):
    res = requests.delete(
        f"{config.url}admin/user/remove/v1",
        json={
            'token' : token,
            'u_id' : u_id,
        }
    )
    return parse_response(res)

def admin_userpermission_change(token, u_id, permission_id):
    res = requests.post(
        f"{config.url}admin/userpermission/change/v1",
        json={
            'token' : token,
            'u_id' : u_id,
            'permission_id' : permission_id,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                               notifications                                   
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def notifications_get(token):
    res = requests.get(
        f"{config.url}notifications/get/v1",
        params={
            'token' : token,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                  search                                       
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def search(token, query_str):
    res = requests.get(
        f"{config.url}search/v1",
        params={
            'token' : token,
            'query_str' : query_str,
        }
    )
    return parse_response(res)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                             testing functions                                 
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# These tests will not run in pipeline, they are just sanity checks to see if
# the file has any typos, etc.

@pytest.mark.parametrize("function, arguments", [
    (auth_login,                    [str(), str()]),
    (auth_register,                 [str(), str(), str(), str()]),
    (auth_logout,                   [str()]),
    (channels_create,               [str(), int(), str()]),
    (channels_list,                 [str()]),
    (channels_listall,              [str()]),
    (channel_details,               [str(), int()]),
    (channel_join,                  [str(), int()]),
    (channel_invite,                [str(), int(), int()]),
    (channel_messages,              [str(), int(), int()]),
    (channel_leave,                 [str(), int()]),
    (channel_addowner,              [str(), int(), int()]),
    (channel_removeowner,           [str(), int(), int()]),
    (message_send,                  [str(), int(), str()]),
    (message_edit,                  [str(), int(), str()]),
    (message_remove,                [str(), int()]),
    (dm_create,                     [str(), list()]),
    (dm_list,                       [str()]),
    (dm_remove,                     [str(), int()]),
    (dm_details,                    [str(), int()]),
    (dm_leave,                      [str(), int()]),
    (dm_messages,                   [str(), int(), int()]),
    (message_senddm,                [str(), int(), str()]),
    (users_all,                     [str()]),
    (user_profile,                  [str(), int()]),
    (user_profile_setname,          [str(), str(), str()]),
    (user_profile_setemail,         [str(), str()]),
    (user_profile_sethandle,        [str(), str()]),
    (admin_user_remove,             [str(), int()]),
    (admin_userpermission_change,   [str(), int(), int()]),
    (notifications_get,             [str()]),
    (search,                        [str(), str()]),
    (message_share,                 [str(), int(), str(), int(), int()]),
    (message_react,                 [str(), int(), int()]),
    (message_unreact,               [str(), int(), int()]),
    (message_pin,                   [str(), int()]),
    (message_unpin,                 [str(), int()]),
    (message_sendlater,             [str(), int(), str(), int()]),
    (message_sendlaterdm,           [str(), int(), str(), int()]),
    (standup_start,                 [str(), int(), int()]),
    (standup_active,                [str(), int()]),
    (standup_send,                  [str(), int(), str()]),
    (auth_passwordreset_reset,      [str(), str()]),
    (user_profile_uploadphoto,      [str(), str(), int(), int(), int(), int()]),
    (user_stats,                    [str()]),
    (users_stats,                   [str()]),
])
def test_successful_route_call(function, arguments):
    # Takes in a function with "sample" arguments of the correct type
    with pytest.raises(HTTPException):
        # Check if the route was at least called
        function(*arguments)


@pytest.mark.parametrize("function, arguments", [
    (clear,                         []),
    (auth_passwordreset_request,    [str()]),
    
])
def test_successful_route_call_no_errors(function, arguments):
    # No errors for these routes, if error is raised something went wrong
    function(*arguments)