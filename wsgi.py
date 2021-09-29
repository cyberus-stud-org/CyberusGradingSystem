from flask import Flask, request, json

from selenium import webdriver

import thm

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome()

app = Flask(__name__)


@app.route('/')
def root():
    return \
        '''<!DOCTYPE html>
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


# check if the user solved the challenge
@app.route('/CheckTHM', methods=['GET', 'POST'])
def check():
    profile = thm.THMProfile(driver, 'WEx90')
    return '<br>'.join(profile.get_all_completed_rooms())


if __name__ == '__main__':
    app.run()
