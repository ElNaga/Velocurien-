import json
from typing import List

class RouteNoeud:
    def __init__(self, json_feature: dict):
        geometry: dict = json_feature['geometry']
        properties: dict = json_feature['properties']
        self.id: int = properties['NODENUM']
        self.type: str = properties['TYPE_NOEUD']
        self.coordonnees: List[float] = geometry['coordinates']

    def to_json(self) -> str:
        schema = {
            "type": "RouteNoeud",
            "properties" : {
                "ID_NOEUD": self.id,
                "TYPE_NOEUD": self.type,
			},
            "geometry" : {
				"type" : "Point",
				"coordinates" : self.coordonnees
			}
        }

        return json.dumps(schema)
