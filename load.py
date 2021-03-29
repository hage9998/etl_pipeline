from pymongo import MongoClient
from pymongo.errors import OperationFailure
import json
def load():
    client = MongoClient()
    try:
        client.list_database_names()
        print('Data Base Connection Established........')

    except OperationFailure as err:
        print(f"Data Base Connection failed. Error: {err}")

    # Database Name
    database_name = client.restaurant
    # Collection Name
    collection_name = database_name.rest
    with open('transformed_data.json') as f:
        file_data = json.load(f)
    collection_name.insert_one(file_data)

