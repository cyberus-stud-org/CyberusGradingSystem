from flask import Flask, request, jsonify
import requests
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

import datetime
import os

from THMGradingSystem import THMGradingSystem
import config

THMGradingSystem = THMGradingSystem()
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=int(os.getenv("JWT_EXPIRES_AFTER_HOURS"))*60)
app.config["JWT_IDENTITY_CLAIM"] = "domain"

jwt = JWTManager(app)


def json_response(msg: str, state: int):
    """convert a message to json format"""
    if state == 0:
        return jsonify({
            "state": "failure",
            "msg": msg
        })

    elif state == 1:
        return jsonify({
            "state": "success",
            "msg": msg
        })


def verify_json_keys(json_data, keys_to_verify):
    """verifies that a list of keys exist in the JSON data and :returns a list of missing keys"""
    missing_kays = []

    # verify JSON data
    for key in keys_to_verify:
        try:
            json_data[key]
        except KeyError:
            missing_kays.append(key)

    return missing_kays


@app.route("/")
def index():
    return ""


@app.route("/api/authenticate", methods=["GET", "POST"])
def authenticate():
    """handles the user authentication process"""
    if request.method == "GET":
        return json_response("No auth credentials provided", 0)
    # get JSON data from request
    try:
        json_data = request.get_json()
    except Exception:
        return jsonify({"msg": "Invalid JSON format"}), 400

    # verify JSON data
    missing_keys = verify_json_keys(json_data, ["domain", "key"])
    if len(missing_keys) > 0:
        return json_response("Missing " + ", ".join(missing_keys), 0), 400

    # return access token if authenticated successfully
    if json_data["domain"] == os.getenv("ALLOWED_DOMAIN") \
            and json_data["key"] == str(os.getenv("API_KEY")):
        access_token = create_access_token(identity=json_data["domain"])
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Invalid username or password"}), 401


@app.route("/api/CheckTHM", methods=["GET", "POST"])
@jwt_required()
def check_thm():
    """check if user solved a specific room on TryHackMe"""
    # get JSON data from request
    try:
        json_data = request.get_json()
    except Exception:
        return json_response("Invalid JSON format", 0), 400

    # verify JSON data
    missing_keys = verify_json_keys(json_data, ["username", "room"])
    if len(missing_keys) > 0:
        return json_response("Missing " + ", ".join(missing_keys), 0), 400

    # check values
    if len(json_data["username"]) > 20 or len(json_data["room"]) > 30:
        return json_response("Invalid Values", 0), 400

    # add room to check to the queue
    result = THMGradingSystem.queue_entry([json_data["username"], json_data["room"]])
    if result:
        return json_response("Added successfully", 1)
    else:
        print(THMGradingSystem.check_driver_status())
        return json_response("Entry Already exists", 0), 400


@app.route("/api/RestartTHM")
@jwt_required()
def restart_thm_system():
    """restart the THM grading system"""
    try:
        THMGradingSystem.driver.close()
        THMGradingSystem.change_driver_status("off")
        return json_response("Restart process executed", 1)
    except Exception:
        return json_response("Unknown error occurred while restarting", 0)


@app.route("/api/CheckCyberTalents", methods=["GET", "POST"])
@jwt_required()
def check_cybertalents():
    """check if user solved a specific challenge on CyberTalents"""
    # get JSON data from request
    try:
        json_data = request.get_json()
    except Exception:
        return json_response("Invalid JSON format", 0), 400

    # verify JSON data
    missing_keys = verify_json_keys(json_data, ["username", "challenge"])
    if len(missing_keys) > 0:
        return json_response("Missing " + ", ".join(missing_keys), 0), 400

    # check values
    if len(json_data["username"]) > 20 or len(json_data["challenge"]) > 30:
        return json_response("Invalid Values", 0), 400

    # check if the user solved the challenge
    response = requests.get(f"{config.CYBERTALENTS_PROFILE_URL}{json_data['username']}/profile")

    if json_data["challenge"] in response.text:
        return json_response("User solved the challenge", 1)
    return json_response("User didn't solve the challenge", 0)


if __name__ == "__main__":
    app.run()
