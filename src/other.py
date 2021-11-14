from src.data_store import data_store
from src.helper import current_timestamp

def clear_v1():
    store = {
        'users': [],
        'channels': [],
        'message_id': 1,
        'dms' : [],
        'workspace_stats' : {
            'channels_exist' : [
                {
                    'num_channels_exist' : 0,
                    'time_stamp' : current_timestamp(),
                },
            ],
            'dms_exist' : [
                {
                    'num_dms_exist' : 0,
                    'time_stamp' : current_timestamp(),
                },
            ],
            'messages_exist' : [
                {
                    'num_messages_exist' : 0,
                    'time_stamp' : current_timestamp(),
                },
            ],
        },
    }
    data_store.set(store)
