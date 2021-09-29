import requests
import config

def check_cybertalents(username, roomname):
    response = requests.get(f'{CYBERTALENTS_PROFILE_URL}{username}/profile')

    if roomname in response.text:
        return True
    else:
        return False


print(check_cybertalents('wasfyelbaz', 'Eye of Sauron'))
