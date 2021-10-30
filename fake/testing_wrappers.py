from werkzeug.exceptions import HTTPException
import pytest
from fake.admin import *
from fake.auth import *
from fake.channel import *
from fake.channels import *
from fake.dm import *
from fake.message import *
from fake.notifications import *
from fake.other import *
from fake.search import *
from fake.standup import *
from fake.user import *
from fake.users import *


@pytest.mark.parametrize("function, arguments", [
    (auth_login,                    [str(), str()]),
    (auth_register,                 [str(), str(), str(), str()]),
    # (auth_logout,                   [str()]),
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
    # (notifications_get,             [str()]),
    # (search,                        [str(), str()]),
    # (message_share,                 [str(), int(), str(), int(), int()]),
    # (message_react,                 [str(), int(), int()]),
    # (message_unreact,               [str(), int(), int()]),
    # (message_pin,                   [str(), int()]),
    # (message_unpin,                 [str(), int()]),
    # (message_sendlater,             [str(), int(), str(), int()]),
    # (message_sendlaterdm,           [str(), int(), str(), int()]),
    # (standup_start,                 [str(), int(), int()]),
    # (standup_active,                [str(), int()]),
    # (standup_send,                  [str(), int(), str()]),
    # (auth_passwordreset_reset,      [str(), str()]),
    # (user_profile_uploadphoto,      [str(), str(), int(), int(), int(), int()]),
    # (user_stats,                    [str()]),
    # (users_stats,                   [str()]),
])
def test_successful_route_call(function, arguments):
    # Takes in a function with "sample" arguments of the correct type
    with pytest.raises(HTTPException):
        # Check if the route was at least called
        function(*arguments)


@pytest.mark.parametrize("function, arguments", [
    (clear,                         []),
    # (auth_passwordreset_request,    [str()]),
    
])
def test_successful_route_call_no_errors(function, arguments):
    # No errors for these routes, if error is raised something went wrong
    function(*arguments)