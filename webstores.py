from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def get_relevant_webstore_data(ingredients):
    # connect to the server with new client
    uri = "mongodb+srv://admin:JKEw0feoZCxOE0LS@cluster0.m5iuzzq.mongodb.net/?retryWrites=true&w=majority" \
          "&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client["webstores"]
    collection = db["webstoreItems"]

    findings = []
    for ing in ingredients:
        findings += list(collection.find({"nname": {"$regex": ing}}))

    return findings
