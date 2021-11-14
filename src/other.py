from src.data_store import data_store
import os 

def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['message_id'] = 1
    store['dms'] = []
    data_store.set(store)
    
    # clear images storage directory 
    images_path = os.path.join(os.getcwd(), 'images')
    if os.path.exists(images_path): 
        
        # delete every file in directory except the default profile picture
        for filename in os.listdir(images_path): 
            if filename != 'default.jpg':
                os.remove(os.path.join(images_path, filename))
