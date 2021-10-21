def dm_list_v1(token):
    store = data_store.get()

    # token validity check
    if token_to_user(token, store) is not None:
        user = token_to_user(token, store)
        # extract the u_id from the user
        u_id = user['u_id']
    else:
        raise AccessError('Invalid token')

    # user validity check
    if check_valid_id(u_id, store) == False:
        raise InputError("Invalid u_id")

    dm_data = []
    # a list of dictionary that we return
    return_dms = {'dms': dm_data}
    dm_data = []

    # check if the user'd u_id is part of the dm,
    # if so, append it to dm_data.
    for dm_id in store['dms']:
        for member in dm_id['members']:
            if u_id == member['u_id']:
                dm = {'dm_id': dm_id['dm_id'], 'name': dm_id['name']}
                dm_data.append(dm)

    return return_dms

