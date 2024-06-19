import json
from typing import Dict, Any

from flask import Flask, request

from test import solve
from webstores import get_relevant_webstore_data, get_possible_units, \
    get_unit_conversions

app = Flask(__name__)


def hello():
    return "Hello world"


def generate_inputfile(raw: Dict[str, Any], items: list):
    instance = ""

    instance += "\n"

    instance += "nutrient(energy).\n"
    instance += "nutrient(protein).\n"
    instance += "nutrient(fat).\n"
    instance += "nutrient(saturates).\n"
    instance += "nutrient(carbs).\n"
    instance += "nutrient(sugar).\n"
    instance += "nutrient(salt).\n"

    instance += "\n"

    for d in raw["day"]:
        instance += f'day("{d}").\n'

    instance += "\n"

    for m in raw["meals"]:
        instance += f'meal({m}).\n'

    for r, ms in raw["meal"].items():
        for m in ms:
            # instance += f"meal({c}).\n"
            instance += f"meal_type({r}, {m}).\n"

    instance += "\n"

    # if there are no items found in the db, that means none of the ingredients were found or there were no
    # ingredients needed to any of the recipes
    if not items:
        instance += f"i_costs(aldi, webstore_is_empty, webstore_is_empty, 0, 0).\n"

    for i in items:
        ingredient_name = ''.join(c for c in str(i['ingredientName']).replace(" ", "_").lower() if (c.isalnum()) | (
                    c == "_"))
        ingredient_tag = str(i['ingredientTag']).replace(" ", "_").replace("-", "_")
        weight = int(i['weight'] * 100)
        # i_costs - ingredient costs e.g. i_costs(milk, 300, 200) = 300 ml milk for £2.00
        instance += f"i_costs(aldi, {ingredient_name}, {ingredient_tag}, {weight}, {i['price']}).\n".replace("'", "")
        # i_unit
        instance += f"i_unit({ingredient_name}, {i['unit']}).\n".replace("'", "")
        # ing_has_nutrient - e.g. ing_has_nutrient(milk, 300, protein, 3) = 300 ml milk has 3g protein
        nutrition_per = str(i['nutrition_per'])
        energy = i['energy']
        fat = i['fat']
        saturates = i['saturates']
        carbs = i['carbs']
        sugar = i['sugars']
        protein = i['protein']
        salt = i['salt']
        if (energy != "UNSPECIFIED") & (fat != "UNSPECIFIED") & (saturates != "UNSPECIFIED") & (
                carbs != "UNSPECIFIED") & (sugar != "UNSPECIFIED") & (protein != "UNSPECIFIED") & (
                salt != "UNSPECIFIED"):
            energy = int(float(str(i['energy']).removesuffix("kcal")) * 100)
            fat = int(float(str(i['fat']).removeprefix('<').removeprefix('>').removesuffix("g")) * 100)
            saturates = int(float(str(i['saturates']).removeprefix('<').removeprefix('>').removesuffix("g")) * 100)
            carbs = int(float(str(i['carbs']).removeprefix('<').removeprefix('>').removesuffix("g")) * 100)
            sugar = int(float(str(i['sugars']).removeprefix('<').removeprefix('>').removesuffix("g")) * 100)
            protein = int(float(str(i['protein']).removeprefix('<').removeprefix('>').removesuffix("g")) * 100)
            salt = int(float(str(i['salt']).removeprefix('<').removeprefix('>').removesuffix("g")) * 100)
            if nutrition_per == "UNSPECIFIED":
                # nutritional values meant for the entire product
                nutrition_per = weight
            # nutritional values meant for given nutrition_per
            nutrition_per = int(float(str(nutrition_per).removesuffix("g").removesuffix("ml")) * 100)
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, nutrition_per, 'energy', energy}.\n".replace(
                "'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, nutrition_per, 'fat', fat}.\n".replace("'",
                                                                                                                   "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, nutrition_per, 'saturates', saturates}.\n".replace(
                "'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, nutrition_per, 'carbs', carbs}.\n".replace(
                "'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, nutrition_per, 'sugar', sugar}.\n".replace(
                "'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, nutrition_per, 'protein', protein}.\n".replace(
                "'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, nutrition_per, 'salt', salt}.\n".replace(
                "'", "")
        else:
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, 0, 'energy', 0}.\n".replace("'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, 0, 'fat', 0}.\n".replace("'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, 0, 'saturates', 0}.\n".replace("'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, 0, 'carbs', 0}.\n".replace("'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, 0, 'sugar', 0}.\n".replace("'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, 0, 'protein', 0}.\n".replace("'", "")
            instance += f"ing_has_nutrient{ingredient_name, ingredient_tag, 0, 'salt', 0}.\n".replace("'", "")

    instance += "\n"

    for r in raw["recipe"]:
        instance += f"recipe({r}).\n"

    instance += "\n"

    for i, a in raw["pantry_item"].items():
        amount = a[0]
        unit = a[1]
        # if unit is grams or ml, use amount as given
        if (unit == "grams") | (unit == "ml"):
            instance += f"pantry_item({i}, {int(amount * 100)}).\n"
        # else if grams or ml is among the possible units, and conversion is possible, convert the amount
        elif ("grams" in get_possible_units(i)) & (get_unit_conversions(i).get("grams") != 0):
            converted_amount = amount * get_unit_conversions(i).get("grams")
            instance += f"pantry_item({i}, {int(converted_amount * 100)}).\n"
        elif ("ml" in get_possible_units(i)) & (get_unit_conversions(i).get("ml") != 0):
            converted_amount = amount * get_unit_conversions(i).get("ml")
            instance += f"pantry_item({i}, {int(converted_amount * 100)}).\n"
        # otherwise not storing pantry item

    instance += "\n"

    for n, l in raw["nutrient_needed"].items():
        instance += f"nutrient_needed({n}, {l[0] * 100}, {l[1] * 100}).\n"

    instance += "\n"

    for r in raw["needs"]:
        for i, a in raw["needs"][r].items():
            amount = a[0]
            unit = a[1]
            # if unit is grams or ml, use amount as given
            if (unit == "grams") | (unit == "ml"):
                instance += f"needs({r}, {i}, {int(amount * 100)}).\n"
            # else if grams or ml is among the possible units, and conversion is possible, convert the amount
            elif ("grams" in get_possible_units(i)) & (get_unit_conversions(i).get("grams") != 0):
                converted_amount = amount * get_unit_conversions(i).get("grams")
                instance += f"needs({r}, {i}, {int(converted_amount * 100)}).\n"
            elif ("ml" in get_possible_units(i)) & (get_unit_conversions(i).get("ml") != 0):
                converted_amount = amount * get_unit_conversions(i).get("ml")
                instance += f"needs({r}, {i}, {int(converted_amount * 100)}).\n"
            else:
                # cannot make recipe, do not schedule it
                instance += f":- schedule({r}, _, _).\n"

    # for entry in raw["ing_has_nutrient"]:
    #    ingName = entry["ingName"]
    #    ingAmount = entry["ingAmount"]
    #    nutrName = entry["nutrName"]
    #    nutrAmount = entry["nutrAmount"]
    #    instance += f"ing_has_nutrient({ingName}, {ingAmount}, {nutrName}, {nutrAmount}).\n"

    file_w = open("input.txt", "w")
    file_w.write(instance)

    encodings = '''
    
% the amount of times the recipe has been scheduled for the week
schedule_count(R, C) :- C = #count {D,M : schedule(R, D, M)}, recipe(R).

% calculates the amount of nutrient a recipe has
recipe_has_nutrient(R,N,T) :- T = #sum{FA: FA=IA*NA/Q, ing_has_nutrient(_, I, Q, N, NA), needs(R,I,IA)}, recipe(R), nutrient(N).

% decides whether the amount we need to buy of an ingredient is integer or not.
int(R, I, (((A2 * C)-A3) / A1)) :- ((A2 * C)-A3) \ A1 == 0, recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(_, _, I, A1, P), schedule_count(R,C).
% buy amount A of ingredient I for a certain recipe R with total cost of T.
% two cases when it is an integer and when it is not in which case we need to buy 1 more (ceil function)
buy(R, I, A, S, IN, T) :- T = P*A, T > 0, int(R, I, A), recipe(R), i_costs(S, IN, I, A1, P).
buy(R, I, A, S, IN, T) :- T = P*A, T > 0, C > 0, A = (((A2 * C)-A3) / A1)+1, not int(R, I, _), recipe(R), needs(R, I, A2), pantry_item(I, A3), i_costs(S, IN, I, A1, P), schedule_count(R,C).

% total price is the sum of costs of ingredients we need to buy.
total_cost(S) :- S = #sum {T,R,I,A : buy(R, I, A, _, IN, T)}.

% schedule exactly one recipe with correct meal type, for every day for every meal
1 {schedule(R, D, M) : recipe(R), meal_type(R,M)} 1 :- day(D), meal(M).

% do not schedule recipe if it needs an ingredient NOT in pantry or webstore
:- schedule(R, _, _), recipe(R), needs(R, I, AN), not i_costs(_, _, I, _, _), A < AN, pantry_item(I, A).

% ensure that 50-80g of protein is consumed within a day.
%:- #sum {A,R,M : schedule(R,D,M), recipe_has_nutrient(R, N, A)} < A2, nutrient_needed(N,A2, _), day(D), nutrient(N).
%:- #sum {A,R,M: schedule(R,D,M), recipe_has_nutrient(R, N, A)} > A3, nutrient_needed(N,_,A3), day(D), nutrient(N).

daily_nutrient_sum(D, N, S) :- S = #sum {A,R,M : schedule(R,D,M), recipe_has_nutrient(R, N, A)}, day(D), nutrient(N).
%full_nutrient_sum(N, T) :- T = #sum {S,D: daily_nutrient_sum(_, N, S), day(D)}, nutrient(N).

% nutritional difference for the entire week
daily_nutrient_diff(D, N, T) :- T = A2-S, S < A2, nutrient_needed(N,A2, _), day(D), nutrient(N), daily_nutrient_sum(D,N,S).
daily_nutrient_diff(D, N, T) :- T = S-A3, S > A3, nutrient_needed(N,_, A3), day(D), nutrient(N), daily_nutrient_sum(D,N,S).
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
        "vegetables": {
            "tomato": {
                "whole": 1,
                "grams": 123
            },
            "cherry tomato": {
                "whole": 1,
                "grams": 17
            },
            "onion": {
                "whole": 1,
                "grams": 94
            },
            "cucumber": {
                "whole": 1,
                "grams": 201
            },
            "broccoli": {
                "whole": 1,
                "grams": 300
            },
            "pepper": {
                "whole": 1,
                "grams": 144
            },
            "brussels sprout": {
                "whole": 1,
                "grams": 21
            },
            "radish": {
                "whole": 1,
                "grams": 4.5
            },
            "beetroot": {
                "whole": 1,
                "grams": 50
            },
            "bell pepper": {
                "whole": 1,
                "grams": 114
            },
            "zucchini": {
                "pieces": 1,
                "grams": 200
            },
            "pumpkin": {
                "whole": 1,
                "grams": 245
            },
            "asparagus": {
                "whole": 1,
                "grams": 15
            },
            "carrot": {
                "whole": 1,
                "grams": 46
            },
            "baby carrot": {
                "whole": 1,
                "grams": 10
            },
            "parsnip": {
                "whole": 1,
                "grams": 98
            },
            "spring onion": {
                "whole": 1,
                "grams": 15
            },
            "potato": {
                "whole": 1,
                "grams": 173
            },
            "spinach": {
                "whole": 1,
                "grams": 180
            },
            "cauliflower": {
                "whole": 1,
                "grams": 575
            },
            "red onion": {
                "whole": 1,
                "grams": 94
            },
            "courgette": {
                "whole": 1,
                "grams": 200
            },
            "celery": {
                "whole": 1,
                "grams": 40
            },
            "garlic": {
                "whole": 1,
                "cloves": 10,
                "grams": 30
            },
            "sweet potato": {
                "whole": 1,
                "grams": 144
            },
            "eggplant": {
                "whole": 1,
                "grams": 566
            },
            "kale": {
                "whole": 1,
                "grams": 130
            },
            "jalapeno": {
                "whole": 1,
                "grams": 14
            },
            "avocado": {
                "whole": 1,
                "grams": 201
            },
            "sweet corn": {
                "whole": 1,
                "grams": 89
            },
            "cabbage": {
                "whole": 1,
                "grams": 750
            },
            "leek": {
                "whole": 1,
                "grams": 89
            },
            "lettuce": {
                "whole": 1,
                "grams": 539
            },
            "olive": {
                "whole": 1,
                "grams": 3.8
            },
            "green olive": {
                "whole": 1,
                "grams": 2.7
            },
            "black olive": {
                "whole": 1,
                "grams": 3.8
            },
            "pickle": {
                "whole": 1,
                "grams": 35
            },
        },
        "legumes": {
            "peas": {
                "grams": 0
            },
            "lentils": {
                "grams": 0
            },
            "green beans": {
                "whole": 1,
                "grams": 5.5
            },
            "chickpeas": {
                "grams": 0
            },
            "kidney beans": {
                "grams": 0
            },
            "red lentils": {
                "grams": 0
            },
            "green lentils": {
                "grams": 0
            },
            "edamame": {
                "grams": 0
            },
            "red beans": {
                "grams": 0
            },
            "beans": {
                "grams": 0
            },
            "soybeans": {
                "grams": 0
            },
        },
        "fruit": {
            "fruit": {
                "whole": 0,
                "grams": 0
            },
            "dried fruit": {
                "whole": 0,
                "grams": 0
            },
            "apple": {
                "whole": 1,
                "grams": 182
            },
            "lemon": {
                "whole": 1,
                "grams": 84
            },
            "lime": {
                "whole": 1,
                "grams": 67
            },
            "banana": {
                "whole": 1,
                "grams": 118
            },
            "orange": {
                "whole": 1,
                "grams": 140
            },
            "mandarin": {
                "whole": 1,
                "grams": 74
            },
            "tangerine": {
                "whole": 1,
                "grams": 88
            },
            "nectarine": {
                "whole": 1,
                "grams": 156
            },
            "pineapple": {
                "whole": 1,
                "grams": 907
            },
            "mango": {
                "whole": 1,
                "grams": 336
            },
            "peach": {
                "whole": 1,
                "grams": 175
            },
            "date": {
                "whole": 1,
                "grams": 7.1
            },
            "pear": {
                "whole": 1,
                "grams": 178
            },
            "pomegranate": {
                "whole": 1,
                "grams": 282
            },
            "grape": {
                "whole": 1,
                "grams": 4.9
            },
            "melon": {
                "whole": 1,
                "grams": 1800
            },
            "watermelon": {
                "whole": 1,
                "grams": 16000
            },
            "apricot": {
                "whole": 1,
                "grams": 35
            },
            "kiwi": {
                "whole": 1,
                "grams": 69
            },
            "grapefruit": {
                "whole": 1,
                "grams": 246
            },
            "plum": {
                "whole": 1,
                "grams": 66
            },
            "fig": {
                "whole": 1,
                "grams": 50
            },
            "currant": {
                "whole": 0,
                "grams": 0
            },
            "raisin": {
                "whole": 0,
                "grams": 0
            },
            "prune": {
                "whole": 1,
                "grams": 9.5
            },
            "papaya": {
                "whole": 1,
                "grams": 1250
            },
        },
        "berries": {
            "berries": {
                "whole": 0,
                "grams": 0
            },
            "strawberry": {
                "whole": 1,
                "grams": 12
            },
            "blueberry": {
                "whole": 1,
                "grams": 1.36
            },
            "raspberry": {
                "whole": 1,
                "grams": 2
            },
            "cranberry": {
                "whole": 0,
                "grams": 0
            },
            "cherry": {
                "whole": 1,
                "grams": 8.2
            },
            "sour cherry": {
                "whole": 1,
                "grams": 8.2
            },
            "blackberry": {
                "whole": 1,
                "grams": 6.5
            },
            "elderberry": {
                "whole": 0,
                "grams": 0
            }
        },
        "nuts": {
            "nuts": {
                "whole": 0,
                "grams": 0
            },
            "chestnut": {
                "whole": 1,
                "grams": 8.4
            },
            "walnut": {
                "whole": 1,
                "grams": 4
            },
            "hazelnut": {
                "whole": 0,
                "grams": 0
            },
            "pecan": {
                "whole": 1,
                "grams": 1.49
            },
            "peanut": {
                "whole": 1,
                "grams": 1
            },
            "almond": {
                "whole": 1,
                "grams": 1.29
            },
            "cashew": {
                "whole": 1,
                "grams": 1.57
            },
            "pistachio": {
                "whole": 1,
                "grams": 0.7
            },
            "sesame seed": {
                "grams": 0
            },
            "chia seed": {
                "grams": 0
            },
            "pumpkin seed": {
                "whole": 0,
                "grams": 0
            },
            "sunflower seed": {
                "whole": 0,
                "grams": 0
            },
            "poppy seed": {
                "grams": 0
            },
        },
        "mushroom": {
            "mushroom": {
                "whole": 1,
                "grams": 12
            },
            "shiitake mushroom": {
                "whole": 1,
                "grams": 19
            },
            "wild mushroom": {
                "whole": 1,
                "grams": 12
            },
            "chestnut mushroom": {
                "whole": 1,
                "grams": 25
            },
        },
        "grains": {
            "rice": {
                "grams": 0
            },
            "white rice": {
                "grams": 0
            },
            "brown rice": {
                "grams": 0
            },
            "cereal flakes": {
                "grams": 0
            },
            "risotto rice": {
                "grams": 0
            },
            "jasmine rice": {
                "grams": 0
            },
            "bulgur": {
                "grams": 0
            },
            "grits": {
                "grams": 0
            },
            "sushi rice": {
                "grams": 0
            }
        },
        "dairy": {
            "milk": {
                "ml": 100,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "goat milk": {
                "ml": 100,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "egg": {
                "whole": 1,
                "grams": 50
            },
            "duck egg": {
                "whole": 1,
                "grams": 70
            },
            "yogurt": {
                "ml": 100,
                "grams": 104,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "greek yogurt": {
                "ml": 100,
                "grams": 118,
                "tbsp": 6.79,
                "tsp": 20.12
            },
            "cream": {
                "ml": 100,
                "grams": 101,
                "tbsp": 6.76,
                "tsp": 20.28
            },
            "kefir": {
                "ml": 0,
                "grams": 0,
                "tbsp": 0,
                "tsp": 0
            },
            "butter": {
                "grams": 100,
                "tbsp": 7.05,
                "tsp": 21.16
            },
            "sour cream": {
                "ml": 100,
                "grams": 104,
                "tbsp": 6.76,
                "tsp": 20.3
            },
            "whipped cream": {
                "ml": 100,
                "grams": 101,
                "tbsp": 6.76,
                "tsp": 20.3
            },
            "margarine": {
                "grams": 100,
                "tbsp": 7.37,
                "tsp": 22.12
            },
            "custard": {
                "grams": 100,
                "tbsp": 6.56,
                "tsp": 19.67
            },
        },
        "substitutes": {
            "coconut milk": {
                "ml": 100,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "almond milk": {
                "ml": 100,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "soy milk": {
                "ml": 100,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "oat milk": {
                "ml": 100,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "rice milk": {
                "ml": 100,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "cashew milk": {
                "ml": 100,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "non-dairy milk": {
                "ml": 100,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "almond butter": {
                "grams": 100,
                "tbsp": 7.05,
                "tsp": 21.16
            },
            "vegan butter": {
                "grams": 100,
                "tbsp": 7.05,
                "tsp": 21.16
            },
            "coconut butter": {
                "grams": 100,
                "tbsp": 7.05,
                "tsp": 21.16
            },
            "tofu": {
                "grams": 0
            },
            "vegan mayo": {
                "ml": 100,
                "grams": 97.2,
                "tbsp": 6.76,
                "tsp": 20.3
            },
            "non-dairy yogurt": {
                "ml": 100,
                "grams": 104,
                "tbsp": 6.75,
                "tsp": 20.3
            },
            "vegan cheese": {
                "grams": 0
            },
            "vegan sausage": {
                "whole": 1,
                "grams": 56.75
            },
            "vegan bacon": {
                "whole": 1,
                "grams": 21
            },
            "quorn": {
                "grams": 0
            }
        },
        "bakery": {
            "bread": {
                "whole": 1,
                "slices": 22,
                "grams": 0
            },
            "tortilla": {
                "whole": 0
            },
            "baguette": {
                "whole": 0,
                "grams": 0
            },
            "pita": {
                "whole": 0
            },
            "sourdough": {
                "whole": 0,
                "grams": 0
            },
            "brioche": {
                "whole": 0,
                "grams": 0
            },
            "bagel": {
                "whole": 0,
                "grams": 0
            },
            "croissant": {
                "whole": 0
            },
            "garlic bread": {
                "whole": 0,
                "grams": 0
            },
            "crumpet": {
                "whole": 0,
                "grams": 0
            }
        },
        "cheese": {
            "cheese": {
                "block": 0,
                "grams": 0
            },
            "parmesan": {
                "block": 0,
                "grams": 0
            },
            "cream cheese": {
                "ml": 100,
                "grams": 95.1,
                "tbsp": 7.11,
                "tsp": 21.3
            },
            "cheddar": {
                "block": 0,
                "grams": 0
            },
            "mozzarella": {
                "ball": 0,
                "grams": 0
            },
            "feta": {
                "block": 0,
                "grams": 0
            },
            "goat cheese": {
                "block": 0,
                "grams": 0
            },
            "mascarpone": {
                "grams": 100,
                "tbsp": 7.11,
                "tsp": 21.3
            },
            "cottage cheese": {
                "grams": 100,
                "tbsp": 7.11,
                "tsp": 21.3
            },
            "quark": {
                "grams": 100,
                "tbsp": 7.11,
                "tsp": 21.3
            },
            "halloumi": {
                "block": 0,
                "grams": 0
            },
            "camambert": {
                "whole": 0,
                "grams": 0
            },
            "sot cheese": {
                "grams": 100,
                "tbsp": 7.11,
                "tsp": 21.3
            },
            "edam": {
                "whole": 0,
                "grams": 0
            }
        },
        "pasta": {
            "pasta": {
                "grams": 0
            },
            "macaroni": {
                "grams": 0
            },
            "penne": {
                "grams": 0
            },
            "spaghetti": {
                "grams": 0
            },
            "angel hair pasta": {
                "grams": 0
            },
            "lasagna sheets": {
                "grams": 0
            },
            "noodles": {
                "grams": 0
            },
            "rice noodles": {
                "grams": 0
            },
            "gnocchi": {
                "grams": 0
            }
        },
        "fish": {
            "fish": {
                "whole": 0,
                "grams": 0
            },
            "salmon": {
                "whole": 1,
                "grams": 75
            },
            "smoked salmon": {
                "whole": 1,
                "grams": 75
            },
            "cod": {
                "whole": 0,
                "grams": 0
            },
            "tuna": {
                "whole": 0,
                "grams": 0
            },
            "sea bass": {
                "whole": 0,
                "grams": 0
            },
            "fish fillet": {
                "whole": 0,
                "grams": 0
            },
            "fish fingers": {
                "whole": 1,
                "grams": 49
            },
            "catfish": {
                "whole": 0,
                "grams": 0
            },
            "haddock": {
                "whole": 0,
                "grams": 0
            },
            "caviar": {
                "grams": 0
            },
            "herring": {
                "whole": 0,
                "grams": 0
            }
        },
        "seafood": {
            "prawns": {
                "whole": 1,
                "grams": 5
            },
            "shrimp": {
                "whole": 1,
                "grams": 5
            },
            "eel": {
                "whole": 0,
                "grams": 0
            },
            "crab": {
                "whole": 0,
                "grams": 0
            },
            "scallop": {
                "whole": 1,
                "grams": 13
            },
            "squid": {
                "whole": 1,
                "grams": 150
            },
            "lobster": {
                "whole": 1,
                "grams": 150
            },
            "oyster": {
                "whole": 1,
                "grams": 25
            },
            "octopus": {
                "whole": 0,
                "grams": 0
            },
            "seaweed": {
                "grams": 0
            },
            "nori": {
                "grams": 0
            },
            "kelp": {
                "grams": 0
            },
            "crab stick": {
                "whole": 1,
                "grams": 17.2
            }
        },
        "meat items": {
            "chicken breast": {
                "whole": 1,
                "grams": 189
            },
            "turkey breast": {
                "whole": 0,
                "grams": 0
            },
            "duck breast": {
                "whole": 1,
                "grams": 240
            },
            "chicken thighs": {
                "whole": 1,
                "grams": 130
            },
            "chicken wings": {
                "whole": 1,
                "grams": 26.79
            },
            "whole chicken": {
                "whole": 1,
                "grams": 1500
            },
            "whole turkey": {
                "whole": 0,
                "grams": 0
            },
            "whole duck": {
                "whole": 0,
                "grams": 0
            },
            "bacon": {
                "stripe": 1,
                "grams": 21
            },
            "minced meat": {
                "grams": 0
            },
            "minced beef": {
                "grams": 0
            },
            "minced pork": {
                "grams": 0
            },
            "minced lamb": {
                "grams": 0
            },
            "minced turkey": {
                "grams": 0
            },
            "beef steak": {
                "whole": 1,
                "grams": 221
            },
            "pork shoulder": {
                "whole": 1,
                "grams": 175
            },
            "lamb shoulder": {
                "whole": 1,
                "grams": 210
            },
            "pork loin": {
                "whole": 1,
                "grams": 120
            },
            "lamb loin": {
                "whole": 0,
                "grams": 0
            },
            "pork chops": {
                "whole": 1,
                "grams": 187
            },
            "lamb chops": {
                "whole": 1,
                "grams": 1857
            },
            "leg of lamb": {
                "whole": 1,
                "grams": 1150
            },
            "pulled pork": {
                "grams": 0
            },
            "ribs": {
                "ribs": 0,
                "grams": 0
            },
            "pork ribs": {
                "ribs": 0,
                "grams": 0
            },
            "beef ribs": {
                "ribs": 0,
                "grams": 0
            },
            "pork belly": {
                "grams": 0
            },
            "sausage": {
                "whole": 1,
                "grams": 56.75
            },
            "frankfurter": {
                "whole": 1,
                "grams": 35
            },
            "bratwurst": {
                "whole": 1,
                "grams": 90
            },
            "chorizo": {
                "whole": 1,
                "grams": 200
            },
            "pancetta": {
                "grams": 0
            },
            "chicken nuggets": {
                "nugget": 1,
                "grams": 16
            },
            "meatballs": {
                "whole": 1,
                "grams": 28.35
            },
            "pepperoni": {
                "slices": 1,
                "grams": 4
            },
            "salami": {
                "slice": 1,
                "grams": 9.8
            },
            "ham": {
                "slice": 1,
                "grams": 28
            },
            "burger patty": {
                "whole": 1,
                "grams": 120
            },
            "rabbit": {
                "whole": 0,
                "grams": 0
            },
            "beef": {
                "whole": 0,
                "grams": 0
            },
            "chicken": {
                "whole": 0,
                "grams": 0
            },
            "lamb": {
                "whole": 0,
                "grams": 0
            },
            "duck": {
                "whole": 0,
                "grams": 0
            },
            "goose": {
                "whole": 0,
                "grams": 0
            }
        },
        "spices": {
            "salt": {
                "grams": 100,
                "tbsp": 5.85,
                "tsp": 17.57
            },
            "pepper": {
                "grams": 100,
                "tbsp": 14.49,
                "tsp": 43.48
            },
            "cinnamon": {
                "grams": 100,
                "tbsp": 12.82,
                "tsp": 38.46
            },
            "parsley": {
                "grams": 100,
                "tbsp": 62.5,
                "tsp": 78.95
            },
            "cumin": {
                "grams": 100,
                "tbsp": 16.63,
                "tsp": 50
            },
            "basil": {
                "grams": 100,
                "tbsp": 79.6,
                "tsp": 239
            },
            "thyme": {
                "grams": 100,
                "tbsp": 23.26,
                "tsp": 71
            },
            "ginger": {
                "grams": 0,
                "tbsp": 0,
                "tsp": 0
            },
            "garlic powder": {
                "grams": 100,
                "tbsp": 10.31,
                "tsp": 30.93
            },
            "oregano": {
                "grams": 100,
                "tbsp": 16.66,
                "tsp": 55.55
            },
            "chili flakes": {
                "grams": 100,
                "tbsp": 20,
                "tsp": 100
            },
            "chili powder": {
                "grams": 100,
                "tbsp": 16.92,
                "tsp": 37.04
            },
            "paprika": {
                "grams": 100,
                "tbsp": 14.71,
                "tsp": 43.48
            },
            "rosemary": {
                "grams": 100,
                "tbsp": 30.3,
                "tsp": 83.33
            },
            "bay leaf": {
                "leaves": 1,
                "grams": 0.2,
                "tbsp": 0.11,
                "tsp": 0.33
            },
            "mint": {
                "grams": 100,
                "tbsp": 30.3,
                "tsp": 83.33
            },
            "all season": {
                "grams": 100,
                "tbsp": 14.08,
                "tsp": 41.63
            },
            "white pepper": {
                "grams": 100,
                "tbsp": 14.08,
                "tsp": 41.63
            },
            "nutmeg": {
                "grams": 100,
                "tbsp": 14.08,
                "tsp": 41.63
            },
            "cayenne": {
                "grams": 100,
                "tbsp": 14.08,
                "tsp": 41.63
            },
            "turmeric": {
                "grams": 100,
                "tbsp": 14.08,
                "tsp": 41.63
            },
            "coriander": {
                "grams": 100,
                "tbsp": 14.08,
                "tsp": 41.63
            },
            "marjoram": {
                "grams": 100,
                "tbsp": 14.08,
                "tsp": 41.63
            }
        },
        "baking": {
            "sugar": {
                "grams": 100,
                "tbsp": 8,
                "tsp": 23.81
            },
            "brown sugar": {
                "grams": 100,
                "tbsp": 8,
                "tsp": 23.81
            },
            "granulated sugar": {
                "grams": 100,
                "tbsp": 8,
                "tsp": 23.81
            },
            "maple syrup": {
                "grams": 100,
                "ml": 75.11,
                "tbsp": 6.7,
                "tsp": 20
            },
            "caramel syrup": {
                "grams": 100,
                "tbsp": 4.87,
                "tsp": 15.02
            },
            "chocolate syrup": {
                "grams": 100,
                "tbsp": 4.87,
                "tsp": 15.02
            },
            "golden syrup": {
                "grams": 100,
                "ml": 75.11,
                "tbsp": 6.7,
                "tsp": 20
            },
            "strawberry syrup": {
                "grams": 100,
                "tbsp": 4.87,
                "tsp": 15.02
            },
            "demerara sugar": {
                "grams": 100,
                "tbsp": 8,
                "tsp": 23.81
            },
            "yeast": {
                "grams": 100,
                "tbsp": 1175,
                "tsp": 3174.66
            },
            "flour": {
                "grams": 100,
                "tbsp": 1175,
                "tsp": 12.8
            },
            "self-raising flour": {
                "grams": 100,
                "tbsp": 1175,
                "tsp": 12.8
            },
            "whole wheat flour": {
                "grams": 100,
                "tbsp": 1175,
                "tsp": 12.8
            },
            "vanilla": {
                "grams": 100,
                "ml": 113.74,
                "tbsp": 7.69,
                "tsp": 23.81
            },
            "honey": {
                "grams": 100,
                "ml": 69.6,
                "tbsp": 4.71,
                "tsp": 14.1
            },
            "baking powder": {
                "grams": 100,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "baking soda": {
                "grams": 100,
                "tbsp": 5.88,
                "tsp": 16.66
            },
            "chocolate chips": {
                "grams": 0
            },
            "cocoa powder": {
                "grams": 100,
                "tbsp": 13.1,
                "tsp": 39.4
            },
            "white chocolate": {
                "grams": 0
            },
            "white chocolate chips": {
                "grams": 0
            },
            "dark chocolate chips": {
                "grams": 0
            },
            "mint extract": {
                "grams": 100,
                "ml": 113.74,
                "tbsp": 7.69,
                "tsp": 23.81
            },
            "rum extract": {
                "grams": 100,
                "ml": 113.74,
                "tbsp": 7.69,
                "tsp": 23.81
            },
            "almond extract": {
                "grams": 100,
                "ml": 113.74,
                "tbsp": 7.69,
                "tsp": 23.81
            }
        },
        "cupboard": {
            "breadcrumbs": {
                "grams": 0
            },
            "peanut butter": {
                "grams": 100,
                "tbsp": 6.57,
                "tsp": 19.7
            },
            "jam": {
                "grams": 100,
                "tbsp": 5,
                "tsp": 15
            },
            "raspberry jam": {
                "grams": 100,
                "tbsp": 5,
                "tsp": 15
            },
            "apricot jam": {
                "grams": 100,
                "tbsp": 5,
                "tsp": 15
            },
            "peach jam": {
                "grams": 100,
                "tbsp": 5,
                "tsp": 15
            },
            "strawberry jam": {
                "grams": 100,
                "tbsp": 5,
                "tsp": 15
            },
            "blueberry jam": {
                "grams": 100,
                "tbsp": 5,
                "tsp": 15
            },
            "lady fingers": {
                "whole": 1,
                "grams": 11
            },
            "waffles": {
                "whole": 1,
                "grams": 75
            },
        },
        "drinks": {
            "coffee": {
                "ml": 0,
            },
            "instant coffee": {
                "grams": 0,
            },
            "decaf coffee": {
                "grams": 0,
            },
            "tea": {
                "bags": 0,
                "ml": 0
            },
            "green tea": {
                "bags": 0,
                "ml": 0
            },
            "chamomile tea": {
                "bags": 0,
                "ml": 0
            },
            "jasmine tea": {
                "bags": 0,
                "ml": 0
            },
            "english breakfast tea": {
                "bags": 0,
                "ml": 0
            },
            "earl grey tea": {
                "bags": 0,
                "ml": 0
            },
            "peppermint tea": {
                "bags": 0,
                "ml": 0
            },
            "herbal tea": {
                "bags": 0,
                "ml": 0
            },
            "juice": {
                "ml": 0
            },
            "orange juice": {
                "ml": 0
            },
            "cranberry juice": {
                "ml": 0
            },
            "pineapple juice": {
                "ml": 0
            },
            "apple juice": {
                "ml": 0
            },
            "matcha powder": {
                "grams": 0
            },
            "lemonade": {
                "ml": 0
            },
            "coke": {
                "ml": 0
            },
            "sprite": {
                "ml": 0
            }
        },
        "oils": {
            "oil": {
                "ml": 100,
                "grams": 85,
                "tbsp": 6.76,
                "tsp": 20
            },
            "olive oil": {
                "ml": 100,
                "grams": 85,
                "tbsp": 6.76,
                "tsp": 20
            },
            "extra virgin olive oil": {
                "ml": 100,
                "grams": 85,
                "tbsp": 6.76,
                "tsp": 20
            },
            "vegetable oil": {
                "ml": 100,
                "grams": 85,
                "tbsp": 6.76,
                "tsp": 20
            },
            "sunflower oil": {
                "ml": 100,
                "grams": 85,
                "tbsp": 6.76,
                "tsp": 20
            },
            "rapeseed oil": {
                "ml": 100,
                "grams": 85,
                "tbsp": 6.76,
                "tsp": 20
            },
            "coconut oil": {
                "ml": 100,
                "grams": 85,
                "tbsp": 6.76,
                "tsp": 20
            },
            "cooking spray": {
                "ml": 100,
                "grams": 85,
                "tbsp": 6.76,
                "tsp": 20
            },
            "sesame oil": {
                "ml": 100,
                "grams": 85,
                "tbsp": 6.76,
                "tsp": 20
            },
            "pork fat": {
                "grams": 100,
                "tbsp": 7.8,
                "tsp": 25
            },
            "beef fat": {
                "grams": 100,
                "tbsp": 7.8,
                "tsp": 25,
            },
            "duck fat": {
                "grams": 100,
                "tbsp": 7.8,
                "tsp": 25
            },
            "lamb fat": {
                "grams": 100,
                "tbsp": 7.8,
                "tsp": 25
            },
            "goose fat": {
                "grams": 100,
                "tbsp": 7.8,
                "tsp": 25
            }
        },
        "dressing": {
            "mayo": {
                "ml": 100,
                "grams": 97.2,
                "tbsp": 6.76,
                "tsp": 20.3
            },
            "ketchup": {
                "grams": 100,
                "ml": 105,
                "tbsp": 7.01,
                "tsp": 21
            },
            "bbq sauce": {
                "grams": 100,
                "ml": 105,
                "tbsp": 7.01,
                "tsp": 21
            },
            "mustard": {
                "grams": 100,
                "ml": 105,
                "tbsp": 7.01,
                "tsp": 21
            },
            "vinegar": {
                "grams": 100,
                "ml": 98.99,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "white vinegar": {
                "grams": 100,
                "ml": 98.99,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "balsamic vinegar": {
                "grams": 100,
                "ml": 98.99,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "red wine vinegar": {
                "grams": 100,
                "ml": 98.99,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "white wine vinegar": {
                "grams": 100,
                "ml": 98.99,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "rice wine vinegar": {
                "grams": 100,
                "ml": 98.99,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "malt vinegar": {
                "grams": 100,
                "ml": 98.99,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "soy sauce": {
                "grams": 100,
                "ml": 98.99,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "wholegrain mustard": {
                "grams": 100,
                "ml": 105,
                "tbsp": 7.01,
                "tsp": 21
            },
            "tomato paste": {
                "grams": 100,
                "ml": 105,
                "tbsp": 7.01,
                "tsp": 21
            },
            "tomato sauce": {
                "grams": 100,
                "ml": 105,
                "tbsp": 7.01,
                "tsp": 21
            },
            "salsa": {
                "grams": 100,
                "tbsp": 5.56,
                "tsp": 18.46
            },
            "pesto": {
                "grams": 100,
                "tbsp": 5.56,
                "tsp": 18.46
            },
            "hummus": {
                "grams": 100,
                "tbsp": 5.56,
                "tsp": 19.51
            },
            "gravy": {
                "ml": 0,
                "grams": 0
            },
            "vegetable gravy": {
                "ml": 0,
                "grams": 0
            },
            "beef gravy": {
                "ml": 0,
                "grams": 0
            },
            "liver pate": {
                "grams": 0
            },
            "curry sauce": {
                "grams": 0
            },
            "lemon juice": {
                "grams": 100,
                "ml": 103,
                "tbsp": 6.86,
                "tsp": 20.6
            },
            "lime juice": {
                "grams": 100,
                "ml": 103,
                "tbsp": 6.86,
                "tsp": 20.6
            }
        },
        "soups": {
            "stock": {
                "whole": 1,
                "grams": 10
            },
            "chicken stock": {
                "whole": 1,
                "grams": 10
            },
            "beef stock": {
                "whole": 1,
                "grams": 10
            },
            "vegetable stock": {
                "whole": 1,
                "grams": 10
            },
        },
    }

    return ingredient_catalog


@app.route('/ingredients', methods=["GET", "POST"])
def ingredients():
    if request.method == "POST":
        ret = generate_ingredient_catalog()
        # upload_all_ingredients_to_wish_list_db(ret)
        return ret
    else:
        return '''
                <form action="#" method="post">
                    <textarea name="getcontent"></textarea>
                    <p><input type="submit" value="generate meal plan"/></p>
                </form>
                '''


def generate_json_schedule_smart(ret, items: list):
    json_ret = {"schedule": {}, "buy": {}}
    # get facts (separated by spaces)
    facts = ret.split(' ')

    for fact in facts:
        if fact == "":
            continue
        # for each fact
        # split into pieces[0] = fact name, pieces[1] = parameters (e.g. 'sugar,0,25')
        pieces = fact.removesuffix(')').split('(')
        # save fact name
        fact_name = pieces[0]
        # get current parameters (e.g. 'sugar,0,25')
        params_in_one = pieces[1].removesuffix('\n').removesuffix(')')
        # split the parameters to a list (e.g. ['sugar', '0', '25']
        params = params_in_one.split(',')

        if fact_name == "schedule":
            # e.g. schedule(cereal,"2024-06-18",breakfast)
            recipe = params[0]
            day = params[1]
            meal = params[2]
            json_ret["schedule"].update({
                day: {
                    meal: recipe
                }
            })
        elif fact_name == "buy":
            # e.g. buy(cereal,milk,1,aldi,cowbelle_welsh_semiskimmed_milk_llaeth_cymreig_hanner,215)
            recipe = params[0]
            tag = params[1]
            amount = int(params[2])
            store = params[3]
            name = params[4]
            price = int(params[5])
            for i in items:
                if tag == i['ingredientTag']:
                    weight = int(i['weight'] * amount)
                    category = i['ingredientCategory']
            json_ret["buy"].update({
                tag: {
                    "recipe": recipe,
                    "amount": amount,
                    "store": store,
                    "ingredientName": name,
                    "price": price,
                    "weight": weight,
                    "category": category
                }
            })

    return json_ret


def generate_json_schedule(ret):
    # start JSON with open bracket
    json_ret = "{"
    # get facts (separated by spaces)
    facts = ret.split(' ')

    fact_name_save = ""
    params_save = []

    for fact in facts:
        if fact == "":
            continue
        # for each fact
        # split into pieces[0] = fact name, pieces[1] = parameters (e.g. 'sugar,0,25')
        pieces = fact.removesuffix(')').split('(')
        # save fact name with quotation marks (to make it JSON)
        fact_name = '''"''' + pieces[0] + '''"'''

        # group facts with same fact names
        # assume facts with same names follow each other (NOT scattered around)
        if fact_name_save != fact_name:
            # if previously saved fact name is NOT the current fact name i.e. reached a new fact group
            # and if this is NOT the first fact (group)
            if fact_name_save != "":
                # append previous fact name with the list of saved parameters
                # replace single quotation marks with double to adhere to JSON rules
                json_ret += f"{fact_name_save} : {params_save}".replace("'", '''"''')

                if fact != facts[-1]:
                    # if this is NOT the last fact
                    # insert comma and new line between fact groups
                    json_ret += ",\n"
            # now that we handled the previous fact group, start a new fact group!
            # start new fact group with no members so far
            params_save = []
        # get current parameters (e.g. 'sugar,0,25')
        params_in_one = pieces[1].removesuffix('\n').removesuffix(')')
        # split the parameters to a list (e.g. ['sugar', '0', '25']
        params = params_in_one.split(',')

        # append this list to the parameter list
        params_save.append(params)
        # save this new fact name (might be the same)
        fact_name_save = fact_name

        if fact == facts[-1]:
            # if this is the last fact
            # save last group
            if len(params_save) == 1:
                json_ret += f",\n{fact_name_save} : {params_save}".replace("'", '''"''')
            else:
                json_ret += f"{fact_name_save} : {params_save}".replace("'", '''"''')



    # end JSON with close bracket
    json_ret += "}"

    return json_ret


@app.route('/meal_plan', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        js = request.json

        all_ingredients = get_all_ingredients(js)

        # there were no ingredients requested
        if not all_ingredients:
            return "ERROR: you do not have any recipes. Try adding recipes to your recipebook!"

        # get relevant web scraped ingredients
        web_store = get_relevant_webstore_data(all_ingredients)

        generate_inputfile(js, web_store)

        file = open("input.txt", "r")
        txt = file.read()
        file.close()

        file = open("output.txt", "w")
        file.write("")
        file.close()

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
        ret = file.read().replace('"', '').split('\n')
        file.close()

        # the given constraints are not possible
        if str(res) == "UNSAT":
            return "ERROR: it is not possible to create a meal plan as none satisfies the constraints."
        # second last line has optimum value
        return generate_json_schedule(ret[-2])
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
