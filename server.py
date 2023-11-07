from flask import Flask

from test import test

app = Flask(__name__)


def hello():
    return "Hello world"


@app.route('/')
def hello_world():
    file = open("tmp.txt", "r")
    test_result = str(test())
    return (file.read()) + '\n' + test_result


if __name__ == "__main__":
    hello_world()
