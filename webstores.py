from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import Dict, Any


def get_relevant_webstore_data(ingredients):
    # connect to the server with new client
    uri = "mongodb+srv://admin:JKEw0feoZCxOE0LS@cluster0.m5iuzzq.mongodb.net/?retryWrites=true&w=majority" \
          "&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client["webstores"]
    collection = db["webstoreItems"]

    findings = []
    for ing in ingredients:
        ing = str(ing).replace("_", " ")
        res = list(collection.find({"ingredientTag": ing}))
        if not res:
            continue
        cheapest_name = res[0]['ingredientName']
        cheapest_per_weight = res[0]['price'] / res[0]['weight']
        for r in res:
            price_per_weight = r['price'] / r['weight']
            if price_per_weight < cheapest_per_weight:
                cheapest_name = r['ingredientName']
                cheapest_per_weight = price_per_weight
        fin = list(collection.find({"ingredientTag": ing, "ingredientName": cheapest_name}))
        findings += fin

    return findings


# tester function
def check_if_exists():
    uri = "mongodb+srv://admin:JKEw0feoZCxOE0LS@cluster0.m5iuzzq.mongodb.net/?retryWrites=true&w=majority" \
          "&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client["webstores"]
    collection = db["webstoreWishList"]

    mydict = {
        "ingredientName": "lentils"
    }

    return collection.find_one(mydict) is not None


def get_possible_units(ingredient):
    uri = "mongodb+srv://admin:JKEw0feoZCxOE0LS@cluster0.m5iuzzq.mongodb.net/?retryWrites=true&w=majority" \
          "&appName=Cluster0"

    # Create a new client and connect to the server
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
    except:
        print("ERROR: Could not connect to MongoDB")

    db = client["webstores"]
    wishlist = db["webstoreWishList"]

    ing_entry = wishlist.find_one({"ingredientName": ingredient})
    if ing_entry is not None:
        return ing_entry.get("possibleUnits")
    else:
        return {}


def get_unit_conversions(ingredient):
    uri = "mongodb+srv://admin:JKEw0feoZCxOE0LS@cluster0.m5iuzzq.mongodb.net/?retryWrites=true&w=majority" \
          "&appName=Cluster0"

    # Create a new client and connect to the server
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
    except:
        print("ERROR: Could not connect to MongoDB")

    db = client["webstores"]
    wishlist = db["webstoreWishList"]

    ing_entry = wishlist.find_one({"ingredientName": ingredient})
    if ing_entry is not None:
        return ing_entry.get("unitConversions")
    else:
        return {}


def upload_all_ingredients_to_wish_list_db(ingredients: Dict[str, Any]):
    # connect to the server with new client
    uri = "mongodb+srv://admin:JKEw0feoZCxOE0LS@cluster0.m5iuzzq.mongodb.net/?retryWrites=true&w=majority" \
          "&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client["webstores"]
    collection = db["webstoreWishList"]

    # delete previous items
    collection.delete_many({})

    for cat in ingredients:
        for ing in ingredients[cat]:
            keys = ingredients[cat][ing].keys()
            entries = ingredients[cat][ing]
            keys_list = []

            for k in keys:
                keys_list.append(k)

            mydict = {
                "ingredientName": ing,
                "ingredientCategory": cat,
                "possibleUnits": keys_list,
                "unitConversions": entries
            }
            collection.insert_one(mydict)
