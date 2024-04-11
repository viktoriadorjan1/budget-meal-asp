import json
from typing import Dict, Any

from flask import Flask, request

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from test import solve

app = Flask(__name__)


def hello():
    return "Hello world"


def webscrape():
    print("Webscraping!")
    options = Options()

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Chrome/83.0.4103.116')
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    # Aldi - search for chicken breast
    keyword = "chickenbreast"
    driver.get('https://groceries.aldi.co.uk/en-GB/Search?keywords=' + keyword)

    # accept cookies
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()
    print("Cookies accepted")

    # visits first result
    while True:
        items = driver.find_elements(By.XPATH, "//a[@class='p text-default-font']")
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(items[0])).click()
            break
        except StaleElementReferenceException:
            # refresh the page
            driver.refresh()

    # get details of product
    while True:
        item_name = driver.find_element(By.XPATH, "//h1[@class='my-0']")
        try:
            ActionChains(driver).move_to_element(item_name).perform()
            print("Item name is " + item_name.text)
            break
        except StaleElementReferenceException:
            driver.refresh()

    while True:
        item_weight = driver.find_element(By.XPATH, "//span[@class='text-black-50 font-weight-bold']")
        try:
            ActionChains(driver).move_to_element(item_weight).perform()
            print("Item weight is " + item_weight.text)
            break
        except StaleElementReferenceException:
            driver.refresh()

    while True:
        item_price = driver.find_element(By.XPATH, "//span[@class='product-price h4 m-0 font-weight-bold']")
        try:
            ActionChains(driver).move_to_element(item_price).perform()
            print("Item price is " + str(item_price.text))
            break
        except StaleElementReferenceException:
            driver.refresh()


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

    # instance += "\n"

    # for i in raw["ingredient"]:
    #    instance += f"ingredient({i}).\n"

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


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        webscrape()

        js = request.json
        print(js)

        generate_inputfile(js)

        print("input generated")

        file = open("input.txt", "r")
        txt = file.read()
        file.close()

        file = open("output.txt", "w")
        file.write("")
        file.close()

        res = solve(txt)

        print("solved")

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
    app.run(debug=True, port=2000)
