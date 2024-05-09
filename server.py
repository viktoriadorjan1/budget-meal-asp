import json
from typing import Dict, Any

from flask import Flask, request

from test import solve
from webstores import get_relevant_webstore_data, check_if_exists

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

    # if there are no items found in the db, that means none of the ingredients were found or there were no
    # ingredients needed to any of the recipes
    if not items:
        instance += f"i_costs(webstore_is_empty, 0, 0).\n"

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

    for entry in raw["ing_has_nutrient"]:
        ingName = entry["ingName"]
        ingAmount = entry["ingAmount"]
        nutrName = entry["nutrName"]
        nutrAmount = entry["nutrAmount"]
        instance += f"ing_has_nutrient({ingName}, {ingAmount}, {nutrName}, {nutrAmount}).\n"

    file_w = open("input.txt", "w")
    file_w.write(instance)

    encodings = '''
% the amount of times the recipe has been scheduled for the week
schedule_count(R, C) :- C = #count {D,M : schedule(R, D, M)}, recipe(R).

% calculates the amount of nutrient a recipe has
recipe_has_nutrient(R,N,T) :- T = #sum{FA: ing_has_nutrient(I, Q, N, NA), needs(R,I,IA), FA=((IA*100*NA/Q))/100}, recipe(R), nutrient(N).

% decides whether the amount we need to buy of an ingredient is integer or not.
int(R, I, (((A2 * C)-A3) / A1)) :- (((A2 * C)-A3) * 10 / A1) \ 10 == 0, recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(I, A1, P), schedule_count(R,C).
% buy amount A of ingredient I for a certain recipe R with total cost of T.
% two cases when it is an integer and when it is not in which case we need to buy 1 more (ceil function)
buy(R, I, A, T) :- T = P*A, T > 0, int(R, I, A), recipe(R), i_costs(I, A1, P).
buy(R, I, A, T) :- T = P*A, T > 0, C > 0, A = (((A2 * C)-A3) / A1)+1, not int(R, I, _), recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(I, A1, P), schedule_count(R,C).

% total price is the sum of costs of ingredients we need to buy.
total_cost(S) :- S = #sum {T,R,I,A : buy(R, I, A, T)}.

% schedule exactly one recipe with correct meal type, for every day for every meal
1 {schedule(R, D, M) : recipe(R), meal_type(R,M)} 1 :- day(D), meal(M).

% do not schedule recipe if it needs an ingredient NOT in pantry or webstore
:- schedule(R, _, _), recipe(R), needs(R, I, AN), not i_costs(I, _, _), A < AN, pantry_item(I, A).

% ensure that 50-80g of protein is consumed within a day.
%:- #sum {A,R,M : schedule(R,D,M), recipe_has_nutrient(R, N, A)} < A2, nutrient_needed(N,A2, _), day(D), nutrient(N).
%:- #sum {A,R,M: schedule(R,D,M), recipe_has_nutrient(R, N, A)} > A3, nutrient_needed(N,_,A3), day(D), nutrient(N).

daily_nutrient_sum(D, N, S) :- S = #sum {A,R,M : schedule(R,D,M), recipe_has_nutrient(R, N, A)}, day(D), nutrient(N).
%full_nutrient_sum(N, T) :- T = #sum {S,D: daily_nutrient_sum(_, N, S), day(D)}, nutrient(N).

% nutritional difference for the entire week
daily_nutrient_diff(D, N, T) :- T = A2-S, S < A2, nutrient_needed(N,A2, _), day(D), nutrient(N), daily_nutrient_sum(D,N,S).
daily_nutrient_diff(D, N, T) :- T = A3-S, S > A3, nutrient_needed(N,_, A3), day(D), nutrient(N), daily_nutrient_sum(D,N,S).
daily_nutrient_diff(D, N, 0) :- S >= A2, S <= A3, nutrient_needed(N,A2, A3), day(D), nutrient(N), daily_nutrient_sum(D,N,S).

% minimize the difference of being out of range for nutrients (most important: @2).
#minimize {T @2: T = S, daily_nutrient_diff(_, _, S)}.
% minimize total cost (less important important: @1)
#minimize {T @1 : total_cost(T)}.'''

    file_w.write(encodings)
    file_w.close()


def get_json_content(json_filename: str):
    file = open(json_filename, "r")
    js = json.load(file)
    file.close()

    return json.dumps(js)


def get_all_ingredients(raw: Dict[str, Any]):
    all_ingredients = []
    for i in raw["ingredient"]:
        all_ingredients.append(i)
    return all_ingredients


def generate_ingredient_catalog():
    ingredient_catalog = {
        "vegetables": [
            "tomato",
            "cherry tomato",
            "onion",
            "cucumber",
            "broccoli",
            "pepper",
            "brussels sprout",
            "radish",
            "beetroot",
            "bell pepper",
            "zucchini",
            "pumpkin",
            "asparagus",
            "carrot",
            "baby carrot",
            "parsnip",
            "spring onion",
            "potato",
            "spinach",
            "cauliflower",
            "red onion",
            "courgette",
            "celery",
            "green beans",
            "garlic",
            "sweet potato",
            "aubergine",
            "kale",
            "jalapeno",
            "avocado",
            "sweet corn",
            "cabbage",
            "leek",
            "lettuce",
            "olive",
            "green_olive",
            "black_olive",
            "pickle",
        ],
        "legumes": [
            "peas",
            "lentils",
            "green_bean",
            "chickpea",
            "kidney_beans",
            "red_lentils",
            "green_lentils",
            "edamame",
            "red_beans",
            "beans",
            "soybeans",
        ],
        "fruit": [
            "fruit",
            "dried_fruit",
            "apple",
            "lemon",
            "lime",
            "banana",
            "orange",
            "mandarin",
            "tangerine",
            "nectarine",
            "pineapple",
            "mango",
            "peach",
            "date",
            "coconut",
            "pear",
            "pomegranate",
            "grape",
            "melon",
            "watermelon",
            "apricot",
            "kiwi",
            "grapefruit",
            "plum",
            "fig",
            "currant",
            "raisin",
            "prune",
            "papaya",
        ],
        "berries": [
            "berries",
            "strawberry",
            "blueberry",
            "raspberry",
            "cranberry",
            "cherry",
            "sour_cherry",
            "blackberry",
            "elderberry",
        ],
        "nuts": [
            "nuts",
            "chestnut",
            "walnut",
            "hazelnut",
            "pecan",
            "peanut",
            "almond",
            "cashew",
            "pistachio",
            "sesame_seed",
            "chia_seed",
            "pumpkin_seed",
            "sunflower_seed",
            "poppy_seed",
        ],
        "mushroom": [
            "mushroom",
            "shiitake mushroom",
            "wild mushroom",
            "chestnut mushroom",
        ],
        "grains": [
            "rice",
            "white rice",
            "brown rice",
            "cereal flakes",
            "risotto rice",
            "jasmine rice",
            "bulgur",
            "grits",
            "sushi_rice",
        ],
        "dairy": [
            "milk",
            "goat milk",
            "egg",
            "duck egg",
            "yogurt",
            "greek yogurt",
            "cream",
            "kefir",
            "butter",
            "sour cream",
            "whipped cream",
            "margarine",
            "custard",
        ],
        "substitutes": [
            "coconut milk",
            "almond milk",
            "soy milk",
            "oat milk",
            "rice milk",
            "cashew milk",
            "non-dairy milk",
            "almond butter",
            "vegan butter",
            "coconut butter",
            "tofu",
            "vegan mayo",
            "non-dairy yogurt",
            "vegan cheese",
            "vegan sausage",
            "vegan bacon",
            "quorn",
        ],
        "bakery": [
            "bread",
            "tortilla",
            "baguette",
            "pita",
            "sourdough",
            "brioche",
            "bagel",
            "croissant",
            "garlic bread",
            "crumpet",
        ],
        "cheese": [
            "cheese",
            "parmesan",
            "cream cheese",
            "cheddar",
            "mozzarella",
            "feta",
            "goat cheese",
            "mascarpone",
            "cottage cheese",
            "quark",
            "halloumi",
            "camambert",
            "sot cheese",
            "edam",
        ],
        "pasta": [
            "pasta",
            "macaroni",
            "penne",
            "spaghetti",
            "angel hair pasta",
            "lasagna sheets",
            "noodles",
            "rice_noodles",
            "gnocchi",
        ],
        "fish": [
            "fish",
            "salmon",
            "smoked salmon",
            "cod",
            "tuna",
            "sea bass",
            "fish fillet",
            "fish fingers",
            "catfish",
            "haddock",
            "caviar",
            "herring",
        ],
        "seafood": [
            "prawns",
            "shrimp",
            "eel",
            "crab",
            "scallop",
            "squid",
            "lobster",
            "oyster",
            "octopus",
            "seaweed",
            "nori",
            "kelp",
            "crab stick",
        ],
        "meat items": [
            "chicken breast",
            "turkey breast",
            "duck breast",
            "chicken thighs",
            "chicken wings",
            "whole chicken",
            "whole turkey",
            "whole duck",
            "bacon",
            "minced meat",
            "minced beef",
            "minced pork",
            "minced lamb",
            "minced turkey",
            "beef steak",
            "pork shoulder",
            "lamb shoulder",
            "pork loin",
            "lamb loin",
            "pork chops",
            "lamb chops",
            "leg of lamb",
            "pulled pork",
            "ribs",
            "pork ribs",
            "beef ribs",
            "pork belly",
            "sausage",
            "frankfurter",
            "bratwurst",
            "chorizo",
            "pancetta",
            "chicken nuggets",
            "meatballs",
            "pepperoni",
            "salami",
            "ham",
            "burger patty",
            "rabbit",
            "beef",
            "chicken",
            "lamb",
            "duck",
            "goose",
        ],
        "spices": [
            "salt",
            "pepper",
            "cinnamon",
            "parsley",
            "cumin",
            "basil",
            "thyme",
            "ginger",
            "garlic powder",
            "oregano",
            "chili flakes",
            "chili powder",
            "paprika",
            "rosemary",
            "bay leaf",
            "mint",
            "all season",
            "white pepper",
            "nutmeg",
            "cayenne",
            "turmeric",
            "coriander",
            "marjoram",
        ],
        "baking": [
            "sugar",
            "brown sugar",
            "granulated sugar",
            "maple syrup",
            "caramel syrup",
            "chocolate syrup",
            "golden syrup",
            "strawberry syrup",
            "demerara sugar",
            "yeast",
            "flour",
            "self-raising flour",
            "whole wheat flour",
            "vanilla",
            "honey",
            "baking powder",
            "baking soda",
            "chocolate chips",
            "cocoa powder",
            "white chocolate",
            "white chocolate chips",
            "dark chocolate chips",
            "mint extract",
            "rum extract",
            "almond extract",
        ],
        "cupboard": [
            "breadcrumbs",
            "peanut butter",
            "jam",
            "raspberry jam",
            "apricot jam",
            "peach jam",
            "strawberry jam",
            "blueberry jam",
            "lady fingers",
            "waffles",
        ],
        "drinks": [
            "coffee",
            "instant coffee",
            "decaf coffee",
            "tea",
            "green tea",
            "chamomile tea",
            "jasmine tea",
            "english breakfast tea",
            "earl grey tea",
            "peppermint tea",
            "herbal tea",
            "juice",
            "orange juice",
            "cranberry juice",
            "pineapple juice",
            "apple juice",
            "matcha powder",
            "lemonade",
            "coke",
            "sprite",
        ],
        "oils": [
            "oil",
            "olive oil",
            "extra virgin olive oil",
            "vegetable oil",
            "sunflower oil",
            "rapeseed oil",
            "coconut oil",
            "cooking spray",
            "sesame oil",
            "pork fat",
            "beef fat",
            "duck fat",
            "lamb fat",
            "goose fat",
        ],
        "dressing": [
            "mayo",
            "ketchup",
            "bbq sauce",
            "mustard",
            "vinegar",
            "white vinegar",
            "balsamic vinegar",
            "red_wine vinegar",
            "white wine vinegar",
            "rice wine vinegar",
            "malt vinegar",
            "soy sauce",
            "wholegrain mustard",
            "tomato paste",
            "tomato sauce",
            "salsa",
            "pesto",
            "hummus",
            "gravy",
            "vegetable gravy",
            "beef gravy",
            "liver pate",
            "curry sauce",
            "lemon juice",
            "lime juice",
        ],
        "soups": [
            "stock",
            "chicken stock",
            "beef stock",
            "vegetable stock"
        ],
    }

    return ingredient_catalog


@app.route('/ingredients', methods=["GET", "POST"])
def ingredients():
    if request.method == "POST":
        print("Ingredients")
        ret = generate_ingredient_catalog()
        # print(check_if_exists())
        # upload_all_ingredients_to_wish_list_db(ret)
        return ret
    else:
        return '''
                <form action="#" method="post">
                    <textarea name="getcontent"></textarea>
                    <p><input type="submit" value="generate meal plan"/></p>
                </form>
                '''


@app.route('/meal_plan', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("Received request!")

        js = request.json
        print(js)

        allIngredients = get_all_ingredients(js)

        # there were no ingredients requested
        if not allIngredients:
            return "ERROR: you do not have any recipes. Try adding recipes to your recipebook!"

        # webscrape ingredients
        web_store = get_relevant_webstore_data(allIngredients)

        generate_inputfile(js, web_store)

        file = open("input.txt", "r")
        txt = file.read()
        file.close()

        file = open("output.txt", "w")
        file.write("")
        file.close()

        print(txt)

        res = solve(txt)

        # the database is empty, and you do not have recipes with owned ingredients that satisfy the constraints
        if str(res) == "UNSAT":
            file = open("input.txt", "r")
            txt = file.read()
            if "webstore_is_empty" in txt:
                file.close()
                return "ERROR: the requested ingredients are not in our database, and you do not have recipes with " \
                       "owned ingredients that satisfy the constraints"

        file = open("output.txt", "r")
        ret = file.read()
        file.close()

        # the given constraints are not possible
        if str(res) == "UNSAT":
            return "ERROR: it is not possible to create a meal plan as none satisfies the constraints."

        return ret
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
    app.run(debug=True, host="0.0.0.0", port=9674)
