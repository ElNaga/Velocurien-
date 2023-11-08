import json
from typing import List
from enum import Enum

class ReseauCyclable:
    class TypeDeVoie(Enum):
        CHAUSSEE_DESIGNEE = 1
        ACCOTEMENT_ASPHALTE = 2
        BANDE_CYCLABLE = 3
        PISTE_CYCLABLE_SUR_RUE = 4
        PISTE_CYCLABLE_SITE_PROPRE = 5
        PISTE_CYCLABLE_TROTTOIR = 6
        SENTIER_POLYVALENT = 7
        VELORUE = 8
        VOIE_PARTAGE_BUS_VELO = 9

    class SousTypeVoie(Enum):
        DEFAUT = 0
        CHAUSSEE_ET_CHAUSSEE_CONTRESENS = 11
        CHAUSSEE_BANDE_SENS_CIRCUL = 13
        BANDE_CONTRESENS = 30
        BANDE_CONTRESENS_ET_CHAUSSEE = 31
        BANDE_ET_BANDE_CONTRESENS = 33
        BANDE_HR_PTE = 34
        BANDE_ET_VOIE_BUS_VELO_HR_PTE_UNE_DIR = 35
        BANDE_ET_VOIE_BUS_VELO_HR_PTE = 39
        PISTE_UNIDIRECTIONNELLE = 40
        PISTE_BIDIRECTIONNELLE = 44
        PISTE_SUR_RUE_ET_BANDE_BUS_VELO_HR_PTE = 49
        PISTE_SITE_PROPRE_ET_BANDE_BUS_VELO_HR_PTE = 59
        PISTE_TROTTOIR_ET_BANDE_BUS_VELO_HR_PTE = 69
        VOIE_BUS_VELO_HR_PTE = 94

    class NombreVoies(Enum):
        UNIDIRECTIONNEL = 1
        BIDIRECTIONNEL = 2

    def __init__(self, json_feature: dict):
        geometry: dict = json_feature['geometry']
        properties: dict = json_feature['properties']
        self.id: int = properties['ID_CYCL']
        self.id_geobase: int = properties['ID_TRC']
        self.nb_voies: ReseauCyclable.NombreVoies = self.NombreVoies(properties['NBR_VOIE'])
        self.type_voie: ReseauCyclable.TypeDeVoie = self.TypeDeVoie(properties['TYPE_VOIE_CODE'])
        self.sous_type_voie: ReseauCyclable.SousTypeVoie = self.SousTypeVoie(properties['TYPE_VOIE2_CODE'])
        self.quatre_saisons: bool = properties['SAISONS4']
        self.coordonnees: List[List[float]] = geometry['coordinates']

    def to_json(self) -> str:
        schema = {
            "type": "CyclableSegment",
            "geometry" : {
				"type" : "LineString",
				"coordinates" : self.coordonnees
			},
			"properties" : {
                "ID_PISTE": self.id,
                "ID_GEOBASE": self.id_geobase,
                "TYPE_PISTE": self.type_voie,
                "NB_VOIES": self.nb_voies,
                "QUATRE_SAISONS": self.quatre_saisons
            }
        }

        return json.dumps(schema)
