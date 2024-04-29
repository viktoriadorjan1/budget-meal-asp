import json
from typing import Dict, Any

from flask import Flask, request

from test import solve
from webstores import get_relevant_webstore_data

app = Flask(__name__)


def hello():
    return "Hello world"


def generate_inputfile(raw: Dict[str, Any], items):
    instance = ""

    instance += "day(monday).\n"
    instance += "day(tuesday).\n"

    instance += "\n"

    instance += "nutrient(energy).\n"
    instance += "nutrient(protein).\n"
    instance += "nutrient(fats).\n"
    instance += "nutrient(saturates).\n"
    instance += "nutrient(carbs).\n"
    instance += "nutrient(sugars).\n"
    instance += "nutrient(salt).\n"

    instance += "\n"

    for r, cs in raw["meal"].items():
        for c in cs:
            instance += f"meal({c}).\n"
            instance += f"meal_type({r}, {c}).\n"

    instance += "\n"

    for i in items:
        instance += f"i_costs{i['tag'], i['weight'], i['price']}.\n".replace("'", "")

    instance += "\n"

    for r in raw["recipe"]:
        instance += f"recipe({r}).\n"

    instance += "\n"

    for i, a in raw["pantry_item"].items():
        instance += f"pantry_item({i}, {a}).\n"

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
int(R, I, (((A2 * C)-A3) / A1)) :- (((A2 * C)-A3) * 10 / A1) \ 10 == 0, recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(I, A1, P), schedule_count(R, C).
% buy amount A of ingredient I for a certain recipe R with total cost of T.
% two cases when it is an integer and when it is not in which case we need to buy 1 more (ceil function)
buy(R, I, A, T) :- T = P*A, T > 0, int(R, I, A), recipe(R), i_costs(I, A1, P).
buy(R, I, A, T) :- T = P*A, T > 0, C > 0, A = (((A2 * C)-A3) / A1)+1, not int(R, I, _), recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(I, A1, P), schedule_count(R, C).

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


def get_json_content(json_filename: str):
    file = open(json_filename, "r")
    js = json.load(file)
    file.close()

    return json.dumps(js)


def getIngredients(raw: Dict[str, Any]):
    ingredients = []
    for i in raw["ingredient"]:
        ingredients.append(i)
    return ingredients


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("Received request!")

        js = request.json
        print(js)

        webstore = get_relevant_webstore_data(getIngredients(js))

        generate_inputfile(js, webstore)

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
        # return ''''''
    else:
        raw_str = get_json_content('raw.json')
        return '''
                <form action="#" method="post">
                    <textarea name="getcontent">{raw_str}</textarea>
            	    <p><input type="submit" value="generate meal plan"/></p>
                </form>
                '''.format(raw_str=raw_str)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
