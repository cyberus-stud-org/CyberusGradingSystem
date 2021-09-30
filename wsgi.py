from flask import Flask, request, json

import requests

import thm
import config

driver = thm.start_driver()
app = Flask(__name__)


@app.route('/')
def root():
    return '''
<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>Morse Parse API</title>
            <meta name="description" content="Cyberus Grading System">
        </head>
        <body>
            <p>
                An API grade student's challenges.
            </p>
        </body>
    </html>
    '''


@app.route('/CheckTHM', methods=['GET', 'POST'])
def check_thm():

    global driver

    try:
        json_data = request.json
        json_data['username']
        json_data['room']
    except Exception:
        return 'Error: Invalid JSON', 400

    if len(json_data['username']) > 20 or len(json_data['room']) > 30:
        return 'Error: Invalid Values', 400

    profile = thm.THMProfile(driver, json_data['username'])
    driver = profile.driver

    if profile.username_exists:
        return str(profile.check_if_room_completed(json_data['room'])), 200
    else:
        return 'Error: Username doesn\'t exist', 400


@app.route('/CheckCyberTalents', methods=['GET', 'POST'])
def check_cybertalents():

    try:
        json_data = request.json
        json_data['username']
        json_data['challenge']
    except Exception:
        return 'Error: Invalid JSON', 200

    if len(json_data['username']) > 20 or len(json_data['challenge']) > 30:
        return 'Error: Invalid Values'

    response = requests.get(f'{config.CYBERTALENTS_PROFILE_URL}{json_data["username"]}/profile')

    if json_data["challenge"] in response.text:
        return 'True'
    return 'False'


if __name__ == '__main__':
    app.run()
