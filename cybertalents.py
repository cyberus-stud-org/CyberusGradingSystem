import requests


def check_cybertalents(username, roomname):
    response = requests.get(f'https://cybertalents.com/members/{username}/profile')

    if roomname in response.text:
        return True
    else:
        return False


print(check_cybertalents('wasfyelbaz', 'Eye of Sauron'))
