from flask import Flask, request

from test import test

app = Flask(__name__)


def hello():
    return "Hello world"


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        to_solve = request.form["nm"]
        test_result = str(test(to_solve))
        file = open("tmp.txt", "r")
        return (file.read()) + '\n' + test_result
    else:
        return '''
        <form action="#" method="post">
    	    <p>Name:</p>
    	    <p><input type="text" name="nm" /></p>
    	    <p><input type="submit" value="submit"/></p>
        </form>
        <p>Example:</p>
        <p>motive(harry).<br>
        motive(sally).<br>
        guilty(harry).<br>
        innocent(Suspect) :- motive(Suspect), not guilty(Suspect).</p>
        '''


if __name__ == "__main__":
    app.run(debug=True)
