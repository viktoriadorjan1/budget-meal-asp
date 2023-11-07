from flask import Flask

from test import test

app = Flask(__name__)


def hello():
    return "Hello world"


@app.route('/')
def hello_world():
    test_result = str(test())
    file = open("tmp.txt", "r")
    return (file.read()) + '\n' + test_result


if __name__ == "__main__":
    hello_world()
