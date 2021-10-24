from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper import token_to_user, get_user, is_global_owner

## Properly implementing permissions requires some changes to auth.py
# key lines to notice:
# line 145 - checking if the user should be a global owner or not
# line 157 - adding permissions to users
#
# Furthermore, if a user is a member in a channel but they are a global owner
# they immediately receive the same permissions as owners of the channel
# without actually being in the owner list
# This does not apply to dm/remove/v1 as only the literal original creator
# of the dm can remove the dm

# Overall, a lot of small thing to change around, probably do it as we go
# Notable changes:
#   - Join needs to allow global owners to join any channel
#   - messages edit needs to allow global owners to edit messages despite
#     not being an owner
#   - messages remove edit needs to allow global owners to delete messages
#     despite not being an owner

VALID_PERMISSION_IDS = [1, 2]

def admin_userpermission_change_v1(token, u_id, permission_id):

    store = data_store.get()

    user = token_to_user(token, store)

    if user is None:
        raise AccessError('Invalid token')
    if not is_global_owner(user):
        raise AccessError(
            description = ('User is not a global owner,'
                           'not permitted to change permissions')
        )

    target_user = get_user(u_id, store)

    if target_user is None:
        raise InputError('u_id does not refer to a valid user')

    global_owner_count = 0

    for user in store['users']:
        if is_global_owner(user):
            global_owner_count += 1

    if global_owner_count <= 1 and permission_id == 2:
        raise InputError(
            description = ('Unable to demote global owner to user, '
                           'only 1 global owner left')
        )

    if permission_id not in VALID_PERMISSION_IDS:
        raise InputError('Invalid permission id')

    user['permission_id'] = permission_id

    data_store.set(store)

    return {}

# Need to modify users listall to not return removed members
# listall should check if their email and password is None

# Delete email and password so that user cant login

def admin_user_remove_v1(token, u_id):

    store = data_store.get()

    remover = token_to_user(token, store)

    if remover is None:
        raise AccessError(description='Token is invalid')

    if not is_global_owner(remover):
        raise AccessError(description='User not authorised to remove users')

    user = get_user(u_id, store)

    if user is None:
        raise InputError(description='u_id does not refer to a valid user')

    global_owner_count = 0

    for user in store['users']:
        if is_global_owner(user):
            global_owner_count += 1

    if global_owner_count <= 1 and is_global_owner(user):
        raise InputError(
            description = ('Unable to remove global owner,'
                           'only 1 global owner left')
        )

    # Making emails and handles available for use by other users
    user['email'] = None
    user['password'] = None
    user['handle'] = None
    # Erasing names as per spec instructions
    user['name_first'] = 'Removed'
    user['name_last'] = 'user'
    # Removing contents of messages the user sent
    for dm in store['dms']:
        for message in dm['messages']:
            if message['u_id'] == user['u_id']:
                message['message'] = 'Removed user'
    for channel in store['channels']:
        for message in channel['messages']:
            if message['u_id'] == user['u_id']:
                message['message'] = 'Removed user'
    return {}
