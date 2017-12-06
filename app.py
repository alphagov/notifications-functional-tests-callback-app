import os
from flask import Flask

app = Flask('functional-test-callback-app')

@app.route('/')
def index():
    return 'Functional Test Callback App is running'


@app.route('/callback')
def callback():
    return 'callback route'
