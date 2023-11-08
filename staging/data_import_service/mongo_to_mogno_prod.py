import json
import logging
from mongo_client import update_data_collection

logger = logging.getLogger()

def import_json_to_mongo(json_file, mongo_collection, id_key):
    with open(json_file) as f:
        data = json.load(f)
        update_data_collection(mongo_collection, id_key, data['features'])