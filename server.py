from flask import Flask

app = Flask(__name__)


def hello():
    return "Hello world"


@app.route('/')
def hello_world():
    return "Hello world"
    #hello()
