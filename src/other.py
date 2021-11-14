from src.data_store import data_store
from src.helper import current_timestamp
import os

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
    
    # clear images storage directory 
    images_path = os.path.join(os.getcwd(), 'images')
    if os.path.exists(images_path): 
        
        # delete every file in directory except the default profile picture
        for filename in os.listdir(images_path): 
            if filename != 'default.jpg':
                os.remove(os.path.join(images_path, filename))
