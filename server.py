import json
from typing import Dict, Any

from flask import Flask, request

from test import solve

app = Flask(__name__)


def hello():
    return "Hello world"


def generate_inputfile(raw: Dict[str, Any]):
    instance = ""

    instance += "day(monday).\n"
    instance += "day(tuesday).\n"

    instance += "\n"

    instance += "meal(lunch).\n"
    instance += "meal(dinner).\n"

    instance += "\n"

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
        instance += f"i_costs({i}, {l[0]}, {int(l[1] * 100)}).\n"

    instance += "\n"

    for n, l in raw["nutrient_needed"].items():
        instance += f"nutrient_needed({n}, {l[0]}, {l[1]}).\n"

    instance += "\n"

    for r in raw["needs"]:
        for i, a in raw["needs"][r].items():
            instance += f"needs({r}, {i}, {a}).\n"

    for r in raw["has_nutrient"]:
        for n, a in raw["has_nutrient"][r].items():
            instance += f"has_nutrient({r}, {n}, {a}).\n"

    file_w = open("input.txt", "w")
    file_w.write(instance)

    encodings = '''
% the amount of times the recipe has been scheduled for the week
schedule_count(R, C) :- C = #count {D,M : schedule(R, D, M)}, recipe(R).
        
% decides whether the amount we need to buy of an ingredient is integer or not.
int(R, I, (((A2 * C)-A3) / A1)) :- (((A2 * C)-A3) * 10 / A1) \ 10 == 0, recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(I, A1, P), schedule_count(R,C).
% buy amount A of ingredient I for a certain recipe R with total cost of T.
% two cases when it is an integer and when it is not in which case we need to buy 1 more (ceil function)
buy(R, I, A, T) :- T = P*A, T > 0, int(R, I, A), recipe(R), i_costs(I, A1, P).
buy(R, I, A, T) :- T = P*A, T > 0, C > 0, A = (((A2 * C)-A3) / A1)+1, not int(R, I, _), recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(I, A1, P), schedule_count(R,C).

% total price is the sum of costs of ingredients we need to buy.
total_cost(S) :- S = #sum {T,R,I,A : buy(R, I, A, T)}.

% schedule exactly one cookable recipe for every day for every meal
1 {schedule(R, D, M) : recipe(R)} 1 :- day(D), meal(M).

% ensure that 50-80g of protein is consumed within a day.
:- #sum {A,R,D,M : schedule(R,D,M), has_nutrient(R, N, A)} < A2, nutrient_needed(N,A2, _), nutrient(N).
:- #sum {A,R,D,M : schedule(R,D,M), has_nutrient(R, N, A)} > A3, nutrient_needed(N,_, A3), nutrient(N).

% minimize total cost.
#minimize {T : total_cost(T)}.'''

    file_w.write(encodings)
    file_w.close()


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = open("raw.json", "r")
        js = json.load(file)
        file.close()

        generate_inputfile(js)

        file = open("input.txt", "r")
        txt = file.read()
        file.close()

        file = open("output.txt", "w")
        file.write("")
        file.close()

        res = solve(txt)

        file = open("output.txt", "r")
        ret = file.read()
        file.close()

        return ret + " " + str(res)
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
