from geobase_json_to_mongo import import_json_from_url_to_mongo
from mongo_to_neo4j import import_geobase_to_neo4j
import sys
import os
import logging

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG, handlers=[handler])


PATH_TO_RAW_DATA = os.path.join("/app", "raw_data")

FILES_TO_IMPORT = [ {"routes.json": {
                        'url': "https://donnees.montreal.ca/dataset/984f7a68-ab34-4092-9204-4bdfcca767c5/resource/9d3d60d8-4e7f-493e-8d6a-dcd040319d8d/download/geobase.json",
                        'id_key': "ID_TRC",
                        'collection': "routes_segements"}
                     },
                    {"noeuds.json": 
                        {'url': "https://donnees.montreal.ca/dataset/9bf7932b-2723-4a74-9c34-eb868a0c692f/resource/0bb23d95-94f3-407c-a8ba-802365940778/download/noeud.json",
                        'id_key': "NODENUM",
                        'collection': "routes_noeuds"}
                    },
                    {"reseau_cyclable.geojson": 
                        {'url': "https://donnees.montreal.ca/dataset/5ea29f40-1b5b-4f34-85b3-7c67088ff536/resource/0dc6612a-be66-406b-b2d9-59c9e1c65ebf/download/reseau_cyclable.geojson",
                         'id_key': 'ID_CYCL',
                        'collection': "reseau_cyclable"}
                    },
                    {"businesses.geojson":
                        {'url': "https://donnees.montreal.ca/dataset/c1d65779-d3cb-44e8-af0a-b9f2c5f7766d/resource/ece728c7-6f2d-4a51-a36d-21cd70e0ddc7/download/businesses.geojson",
                         'id_key': 'business_id',
                        'collection': "restaurants"}
                    },
                ]

if __name__ == '__main__':
    for file in FILES_TO_IMPORT:
        for filename, file_info in file.items():
            import_json_from_url_to_mongo(
                file_info['url'],
                PATH_TO_RAW_DATA,
                filename,
                file_info['collection'],
                file_info['id_key']
            )
            
    import_geobase_to_neo4j()
    
    exit(0)
