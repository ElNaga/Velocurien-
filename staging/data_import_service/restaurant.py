import json
from enum import Enum
from typing import List

class Restaurant:
    class Statut(Enum):
        OUVERT = "Ouvert"
        FERME = "Fermé"
        FERME_CHANGEMENT_EXPLOITANT = "Fermé changement d'exploitant"
        EN_TRAITEMENT = "En traitement"
        SOUS_INSPECTION_FEDERALE = "Sous inspection fédérale"

    def __init__(self, json_feature: dict):
        geometry: dict = json_feature['geometry']
        properties: dict = json_feature['properties']
        self.id: int = properties['business_id']
        self.nom: str = properties['name']
        self.type: str = properties['type']
        self.adresse: str = properties['address']
        self.ville: str = properties['city']
        self.province: str = properties['state']
        self.statut: Restaurant.Statut = self.Statut(properties['statut'])
        self.coordonnees: List[float] = geometry['coordinates']

    def to_json(self) -> str:
        schema = {
            "type": "Restaurant",
            "properties" : {
                "ID_RESTAURANT": self.id,
                "NOM": self.nom,
                "STATUT": self.statut,
                "TYPE_RESTAURANT": self.type,
                "ADRESSE": self.adresse,
                "VILLE": self.ville,
                "PROVINCE": self.province
			},
            "geometry" : {
				"type" : "Point",
				"coordinates" : self.coordonnees
			}
        }

        return json.dumps(schema)