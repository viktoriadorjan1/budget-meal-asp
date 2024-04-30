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


def generate_ingredient_catalog():
    ingredient_catalog = {
        "vegetables": [
            "tomato",
            "cherry_tomato",
            "onion",
            "cucumber",
            "broccoli",
            "pepper",
            "brussels_sprout",
            "radish",
            "beetroot",
            "bell_pepper",
            "zucchini",
            "pumpkin",
            "asparagus",
            "carrot",
            "baby_carrot",
            "parsnip",
            "spring_onion",
            "potato",
            "spinach",
            "cauliflower",
            "red_onion",
            "courgette",
            "celery",
            "green_beans",
            "garlic",
            "sweet_potato",
            "aubergine",
            "kale",
            "jalapeno",
            "avocado",
            "sweet_corn",
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
            "shiitake_mushroom",
            "wild_mushroom",
            "chestnut_mushroom",
        ],
        "grains": [
            "rice",
            "white_rice",
            "brown_rice",
            "cereal_flakes",
            "risotto_rice",
            "jasmine_rice",
            "bulgur",
            "grits",
            "sushi_rice",
        ],
        "dairy": [
            "milk",
            "goat_milk",
            "egg",
            "duck_egg",
            "yogurt",
            "greek_yogurt",
            "cream",
            "kefir",
            "butter",
            "sour_cream",
            "whipped_cream",
            "margarine",
            "custard",
        ],
        "substitutes": [
            "coconut_milk",
            "almond_milk",
            "soy_milk",
            "oat_milk",
            "rice_milk",
            "cashew_milk",
            "non-dairy_milk",
            "almond_butter",
            "vegan_butter",
            "coconut_butter",
            "tofu",
            "vegan_mayo",
            "non-dairy_yogurt",
            "vegan_cheese",
            "vegan_sausage",
            "vegan_bacon",
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
            "garlic_bread",
            "crumpet",
        ],
        "cheese": [
            "cheese",
            "parmesan",
            "cream_cheese",
            "cheddar",
            "mozzarella",
            "feta",
            "goat_cheese",
            "mascarpone",
            "cottage_cheese",
            "quark",
            "halloumi",
            "camambert",
            "sot_cheese",
            "edam",
        ],
        "pasta": [
            "pasta",
            "macaroni",
            "penne",
            "spaghetti",
            "angel_hair",
            "lasagna_sheets",
            "noodles",
            "rice_noodles",
            "gnocchi",
        ],
        "fish": [
            "fish",
            "salmon",
            "smoked_salmon",
            "cod",
            "tuna",
            "sea_bass",
            "fish_fillet",
            "fish_fingers",
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
            "crab_stick",
        ],
        "meat_items": [
            "chicken_breast",
            "turkey_breast",
            "duck_breast",
            "chicken_thighs",
            "chicken_wings",
            "whole_chicken",
            "whole_turkey",
            "whole_duck",
            "bacon",
            "minced_meat",
            "minced_beef",
            "minced_pork",
            "minced_lamb",
            "minced_turkey",
            "beef_steak",
            "pork_shoulder",
            "lamb_shoulder",
            "pork_loin",
            "lamb_loin",
            "pork_chops",
            "lamb_chops",
            "leg_of_lamb",
            "pulled_pork",
            "ribs",
            "pork_ribs",
            "beef_ribs",
            "pork_belly",
            "sausage",
            "frankfurter",
            "bratwurst",
            "chorizo",
            "pancetta",
            "chicken_nuggets",
            "meatballs",
            "pepperoni",
            "salami",
            "ham",
            "burger_patty",
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
            "garlic_powder",
            "oregano",
            "chili_flakes",
            "chili_powder",
            "paprika",
            "rosemary",
            "bay_leaf",
            "mint",
            "all_season",
            "white_pepper",
            "nutmeg",
            "cayenne",
            "turmeric",
            "coriander",
            "marjoram",
        ],
        "baking": [
            "sugar",
            "brown_sugar",
            "granulated_sugar",
            "maple_syrup",
            "caramel_syrup",
            "chocolate_syrup",
            "golden_syrup",
            "strawberry_syrup",
            "demerara_sugar",
            "yeast",
            "flour",
            "self-raising_flour",
            "whole_wheat_flour",
            "vanilla",
            "honey",
            "baking_powder",
            "baking_soda",
            "chocolate_chips",
            "cocoa_powder",
            "white_chocolate",
            "white_chocolate_chips",
            "dark_chocolate_chips",
            "mint_extract",
            "rum_extract",
            "almond_extract",
        ],
        "cupboard": [
            "breadcrumbs",
            "peanut_butter",
            "jam",
            "raspberry_jam",
            "apricot_jam",
            "peach_jam",
            "strawberry_jam",
            "blueberry_jam",
            "lady_fingers",
            "waffles",
        ],
        "drinks": [
            "coffee",
            "instant_coffee",
            "decaf_coffee",
            "tea",
            "green_tea",
            "chamomile_tea",
            "jasmine_tea",
            "english_breakfast_tea",
            "earl_grey_tea",
            "peppermint_tea",
            "herbal_tea",
            "juice",
            "orange_juice",
            "cranberry_juice",
            "pineapple_juice",
            "apple_juice",
            "matcha_powder",
            "lemonade",
            "coke",
            "sprite",
        ],
        "oils": [
            "oil",
            "olive_oil",
            "extra_virgin_olive_oil",
            "vegetable_oil",
            "sunflower_oil",
            "rapeseed_oil",
            "coconut_oil",
            "cooking_spray",
            "sesame_oil",
            "pork_fat",
            "beef_fat",
            "duck_fat",
            "lamb_fat",
            "goose_fat",
        ],
        "dressing": [
            "mayo",
            "ketchup",
            "bbq_sauce",
            "mustard",
            "vinegar",
            "white_vinegar",
            "balsamic_vinegar",
            "red_wine_vinegar",
            "white_wine_vinegar",
            "rice_wine_vinegar",
            "malt_vinegar",
            "soy_sauce",
            "wholegrain_mustard",
            "tomato_paste",
            "tomato_sauce",
            "salsa",
            "pesto",
            "hummus",
            "gravy",
            "vegetable_gravy",
            "beef_gravy",
            "liver_pate",
            "curry_sauce",
            "lemon_juice",
            "lime_juice",
        ],
        "soups": [
            "chicken_stock",
            "beef_stock",
            "vegetable_stock"
        ],
    }

    return ingredient_catalog


@app.route('/ingredients', methods=["GET", "POST"])
def ingredients():
    if request.method == "POST":
        print("Ingredients")
        ret = generate_ingredient_catalog()
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
    app.run(debug=True, host="0.0.0.0", port=9674)
