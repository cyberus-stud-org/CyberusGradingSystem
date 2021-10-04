from flask import Flask, request, jsonify
import requests

from THMGradingSystem import THMGradingSystem
import config

THMGradingSystem = THMGradingSystem()
app = Flask(__name__)


def response(msg: str, state: int):

    if state == 0:
        return jsonify({
            'state': 'failure',
            'msg': msg
        })

    elif state == 1:
        return jsonify({
            'state': 'success',
            'msg': msg
        })


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

    try:
        json_data = request.json
        json_data['username']
        json_data['room']
    except Exception:
        return response('Invalid JSON', 0), 400

    if len(json_data['username']) > 20 or len(json_data['room']) > 30:
        return response('Invalid Values', 0), 400

    result = THMGradingSystem.queue_entry([json_data['username'], json_data['room']])
    if result:
        return response('Added successfully', 1)
    else:
        print(THMGradingSystem.check_driver_status())
        return response('Entry Already exists', 0)


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


@app.route('/ResetTHM')
def reset_thm():

    try:
        THMGradingSystem.driver.close()
        THMGradingSystem.change_driver_status('off')
        return response('Reset is being handled', 1)
    except Exception:
        return response('Unknown error occurred while reset', 0)


if __name__ == '__main__':
    app.run()
