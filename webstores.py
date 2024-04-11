from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi


def get_relevant_webstore_data(ingredients):
    #ca = certifi.where()

    # connect to the server with new client
    uri = "mongodb+srv://admin:JKEw0feoZCxOE0LS@cluster0.m5iuzzq.mongodb.net/?retryWrites=true&w=majority" \
          "&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1')) #, tlsCAFile=ca)

    db = client["webstores"]
    collection = db["webstoreItems"]

    findings = []
    for ing in ingredients:
        findings += list(collection.find({"nname": {"$regex": ing}}))

    return findings
