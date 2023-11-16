from typing import Dict, Any

from flask import Flask, request

from test import test

app = Flask(__name__)


def hello():
    return "Hello world"


def generate_inputfile(raw: Dict[str, Any]):
    instance = ""

    for r in raw["recipe"]:
        instance += f"recipe({r}).\n"

    instance += "\n"

    for i in raw["ingredient"]:
        instance += f"ingredient({i}).\n"

    instance += "\n"

    for n in raw["nutrient"]:
        instance += f"nutrient({n}).\n"

    instance += "\n"

    for i, a in raw["pantry_item"].items():
        instance += f"pantry_item({i}, {a}).\n"

    instance += "\n"

    for i, l in raw["i_costs"].items():
        instance += f"i_costs({i}, {l[0]}, {l[1]}).\n"

    instance += "\n"

    for n, l in raw["nutrient_needed"].items():
        instance += f"nutrient_needed({n}, {l[0]}, {l[1]}).\n"

    instance += "\n"

    for n in raw["needs"].items():
        for i, a in n.items():
            instance += f"needs({n}, {i}, {a}).\n"

    instance += "\n"

    file_w = open("input.txt", "w")
    file_w.write(instance)
    file_w.close()


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # to_solve = request.form["nm"]
        generate_inputfile("raw.json")
        test_result = str(test())
        file = open("output.txt", "r")
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
