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
        res = list(collection.find({"ingredientTag": ing}))
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
            #print(f"{cat}: {ing} with {keys} and {entries}")

            for k in keys:
                keys_list.append(k)
                #print(k)

            mydict = {
                "ingredientName": ing,
                "ingredientCategory": cat,
                "possibleUnits": keys_list,
                "unitConversions": entries
            }
            #print(mydict)
            collection.insert_one(mydict)
