from pymongo import MongoClient

def copy_from_staging_to_prod(staging_uri, prod_uri, db_name):
    stagedb_name = "velocurien_staging"
    prod_db_name = "velocurien"

    # Connect to the staging database
    staging_client = MongoClient(staging_uri)
    staging_db = staging_client[stagedb_name]
    
    # Connect to the production database
    prod_client = MongoClient(prod_uri)
    prod_db = prod_client[prod_db_name]
    
    # Assuming we are copying collections wholesale and db_name is the same for staging and prod
    for collection_name in staging_db.list_collection_names():
        staging_collection = staging_db[collection_name]
        prod_collection = prod_db[collection_name]

        # Clear the production collection to avoid duplicates
        # prod_collection.delete_many({})

        # Copy all documents from staging to production
        documents = list(prod_collection.find())
        if documents:
            staging_collection.insert_many(documents)
    
    # Close the connections
    staging_client.close()
    prod_client.close()
