from src.error import InputError, AccessError

def parse_response(response):
    if response.status_code in [200, 201]:
        return response.json()
    elif response.status_code == 400:
        raise InputError()
    elif response.status_code == 403:
        raise AccessError()
    else:
        raise Exception(response)