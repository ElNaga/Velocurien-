import json
import os
import logging
from mongo_client import update_data_collection
from download_json import download_json

logger = logging.getLogger()

def import_json_from_url_to_mongo(url, folder_path, json_file, mongo_collection, id_key):
    if download_json(url, folder_path, json_file):
        logger.info("Importing " + json_file + " to " + mongo_collection)
        import_json_to_mongo(os.path.join(folder_path, json_file), mongo_collection, id_key)

def import_json_to_mongo(json_file, mongo_collection, id_key):
    with open(json_file) as f:
        data = json.load(f)
        update_data_collection(mongo_collection, id_key, data['features'])
