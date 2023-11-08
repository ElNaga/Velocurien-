import os
import logging
from pymongo import MongoClient, collection, cursor

DEFAULT_MONOGO_HOST = 'stagingDB'
DEFAULT_MONOGO_PORT = 27017
DEFAULT_MONOGO_DB = 'velocurien_staging'

logger = logging.getLogger()

mongo_host = os.getenv('MONGO_STAGING_HOST', DEFAULT_MONOGO_HOST)
mongo_port = int(os.getenv('MONGO_STAGING_PORT', DEFAULT_MONOGO_PORT))
mongo_db = os.getenv('MONGO_STAGING_DB', DEFAULT_MONOGO_DB)
client: MongoClient = None

def _connect_to_mongo(mongo_host: str, mongo_port: int, mongo_db: str, mongo_collection: str) -> collection.Collection:
    global client
    client = MongoClient(mongo_host, mongo_port)
    
    db = client[mongo_db]
    collection = db[mongo_collection]
    return collection

def update_data_collection(collection_name: str, id_key: str, data: str) -> None:
    collection = _connect_to_mongo(mongo_host, mongo_port, mongo_db, collection_name)
    
    if collection.count_documents({}) == 0:
        logger.info("Initializing collection " + collection_name + "...")
        _initialize_data_collection(collection, id_key, data)
    else:
        logger.info("Updating collection " + collection_name + "...")
        _insert_if_not_exists(collection, id_key, data)
        _remove_if_not_in_data(collection, id_key, data)
    
    client.close()

def _initialize_data_collection(collection: collection.Collection, id_key: str, data: str) -> None:
    collection.create_index(id_key)
    collection.insert_many(data)
    
def _insert_if_not_exists(collection: collection.Collection, id_key: str, data: str) -> None:
    for item in data:
        collection.update_one({id_key: item['properties'][id_key]}, {"$set": item}, upsert=True)

def _remove_if_not_in_data(collection: collection.Collection, id_key: str, data: str) -> None:
    collection.delete_many({id_key: {"$nin": [item['properties'][id_key] for item in data]}})

def get_cursor_from_collection(collection_name: str) -> cursor.Cursor:
    collection = _connect_to_mongo(mongo_host, mongo_port, mongo_db, collection_name)
    return collection.find()
