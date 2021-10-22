from src.data_store import data_store

def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['dms'] = []
<<<<<<< HEAD
    store['message_id'] = 1
=======
>>>>>>> added files that was not git added before
    data_store.set(store)
