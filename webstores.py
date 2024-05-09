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
        findings += list(collection.find({"tag": {"$regex": ing}}))

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

    for cat in ingredients:
        for ing in ingredients[cat]:
            print(f"{cat}: {ing}")
            mydict = {
                "ingredientName": ing,
                "ingredientCategory": cat
            }
            collection.insert_one(mydict)
