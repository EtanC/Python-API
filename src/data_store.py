import json
'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW (double check later)
initial_object = {
    'users': [],
    'channels': [],
    'message_id': 1,
    'dms' : []
}
## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    def __init__(self):
        try:
            # Read data from data_store.json file
            with open("data_store.json", "r") as FILE:
                store = json.load(FILE)
                self.__store = store
        except json.decoder.JSONDecodeError:
            # If data_store.json doesn't contain valid json or is empty
            # reset data to initial_object
            with open("data_store.json", "w") as FILE:
                json.dump(initial_object, FILE)
            self.__store = initial_object
        except FileNotFoundError:
            # If file does not exist, reset data to initial_object
            with open("data_store.json", "x") as FILE:
                json.dump(initial_object, FILE)
            self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        # Write the data in "store" to the file as json
        with open("data_store.json", "w") as FILE:
            json.dump(store, FILE)
            self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()

