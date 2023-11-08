from enum import Enum
import json
from typing import List
from geojson_length import calculate_distance, Unit
from geojson import Feature


class RouteSegment:
    class Sens(Enum):
        SENS_UNIQUE_INVERSE = -1
        DOUBLE_SENS = 0
        SENS_UNIQUE = 1

    class Classe(Enum):
        RUE_LOCALE = 0
        VOIE_PIETONNIERE = 1
        PLACE_AFFAIRE = 2
        QUAI = 3
        PRIVEE = 4
        COLLECTRICE = 5
        ARTERE_SECONDAIRE = 6
        ARTERE_RINCIPALE = 7
        AUTOROUTE = 8
        PROJETEE = 9

    class Position(Enum):
        PONT = 1
        VIADUC = 2
        VIADUC_SOUS_VIADUC_2 = 3
        VIADUC_SOUS_VIADUC_3 = 4
        SOL = 5
        PASSAGE_SOUS_TRONCON = 6
        TUNNEL = 7
        TUNNEL_SOUS_TUNNEL_7 = 8
        TUNNEL_SOUS_TUNNEL_8 = 9

    def __init__(self, json_feature: dict) -> None:
        geometry: dict = json_feature['geometry']
        properties: dict = json_feature['properties']
        self.id: int = properties['ID_TRC']
        self.nom: str = self.parse_nom_route(properties)
        self.coordonnees: List[List[float]] = geometry['coordinates']
        self.longueur: float = calculate_distance(Feature(geometry=geometry), Unit.meters)
        self.debut_numeros_gauche: int = properties['DEB_GCH']
        self.fin_numeros_gauche: int = properties['FIN_GCH']
        self.debut_numeros_droite: int = properties['DEB_DRT']
        self.fin_numeros_droite: int = properties['FIN_DRT']
        self.classe: RouteSegment.Classe = self.Classe(properties['CLASSE'])
        self.sens: RouteSegment.Sens = self.Sens(properties['SENS_CIR'])
        self.position: RouteSegment.Position = self.Position(properties['POSITION'])

    def parse_nom_route(self, properties: dict) -> str:
        parties_nom_route:List[str] = []

        if properties['TYP_VOIE']: parties_nom_route.append(properties['TYP_VOIE'])
        if properties['LIE_VOIE']: parties_nom_route.append(properties['LIE_VOIE'])
        if properties['NOM_VOIE']: parties_nom_route.append(properties['NOM_VOIE'])
        if properties['DIR_VOIE']: parties_nom_route.append(properties['DIR_VOIE'])

        return ' '.join(parties_nom_route)

    def to_json(self) -> str:
        schema = {
            "type": "RouteSegment",
            "geometry" : {
				"type" : "LineString",
				"coordinates" : self.coordonnees
			},
			"properties" : {
                "ID_ROUTE": self.id,
                "LONGUEUR": self.longueur,
                "NOM_ROUTE": self.nom,
                "NUMEROS_CIVIQUES": {
                    "DEBUT_GAUCHE": self.debut_numeros_gauche,
                    "FIN_GAUCHE": self.fin_numeros_gauche,
                    "DEBUT_DROITE": self.debut_numeros_droite,
                    "FIN_DROITE": self.fin_numeros_droite
                },
                "CLASSE_ROUTE": self.classe,
                "SENS_CIRCULATION": self.sens,
                "POSITION_ROUTE": self.position 
            }
        }
        return json.dumps(schema)
