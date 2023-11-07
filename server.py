from flask import Flask

from test import test

app = Flask(__name__)


def hello():
    return "Hello world"


@app.route('/')
def hello_world():
    return str(test())
