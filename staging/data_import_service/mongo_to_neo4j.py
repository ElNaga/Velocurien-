import os
from py2neo import Graph, Node, Relationship
import mongo_client
import route_segment
import route_noeud
import logging

DEFAULT_URL = "bolt://localhost:7687"

logger = logging.getLogger()

neo4j_host = os.getenv('NEO4J_URL', DEFAULT_URL)
neo4j_user = os.getenv('NEO4J_USER')
neo4j_pwd = os.getenv('NEO4J_PWD')

graphdb = Graph(neo4j_host, auth=(neo4j_user, neo4j_pwd), secure=False)

def import_geobase_to_neo4j():
    noeuds = {}
    logger.info("Parsing nodes...")
    cursor_noeuds = mongo_client.get_cursor_from_collection('routes_noeuds')
    for document in cursor_noeuds:
        noeud = route_noeud.RouteNoeud(document)
        noeuds[(noeud.coordonnees[0], noeud.coordonnees[1])] = noeud
    logger.info("Parsed {} nodes.".format(len(noeuds)))

    logger.info("Importing nodes in Neo4j.")
    neo4j_nodes_transaction = graphdb.begin()
    nb_noeuds = 0
    for noeud in noeuds.values():
        neo4j_nodes_transaction.create(Node("RouteNoeud", id = noeud.id, type = noeud.type, longitude = noeud.coordonnees[0], latitude = noeud.coordonnees[1]))
        nb_noeuds = nb_noeuds + 1
        if nb_noeuds % 1000 == 0:
            graphdb.commit(neo4j_nodes_transaction)
            neo4j_nodes_transaction = graphdb.begin()
            logger.info("Still running. {} nodes completed.".format(nb_noeuds))
    graphdb.commit(neo4j_nodes_transaction)

    logger.info("Parsing edges...")
    segments = []
    cursor_segments = mongo_client.get_cursor_from_collection('routes_segements')
    for document in cursor_segments:
        segment = route_segment.RouteSegment(document)
        segments.append(segment)
    logger.info("Parsed {} edges.".format(len(segments)))

    logger.info("Merging nodes and edges...")
    nb_segments = 0
    neo4j_edges_transaction = graphdb.begin()
    for segment in segments:
        try:
            noeud_a = graphdb.nodes.match("RouteNoeud", longitude=segment.coordonnees[0][0], latitude=segment.coordonnees[0][1])
            noeud_b = graphdb.nodes.match("RouteNoeud", longitude=segment.coordonnees[len(segment.coordonnees)-1][0], latitude=segment.coordonnees[len(segment.coordonnees)-1][1])
            
            if noeud_a is not None and noeud_b is not None:
                neo4j_edges_transaction.create(Relationship(noeud_a, "RouteSegment", noeud_b, 
                                            id = segment.id,
                                            nom = segment.nom, 
                                            longueur = segment.longueur,
                                            classe = segment.classe.name, 
                                            sens = segment.sens.name, 
                                            position = segment.position.name,
                                            debut_numeros_gauche = segment.debut_numeros_gauche,
                                            fin_numeros_gauche = segment.fin_numeros_gauche,
                                            debut_numeros_droite = segment.debut_numeros_droite,
                                            fin_numeros_droite = segment.fin_numeros_droite))
                nb_segments = nb_segments+1
            if nb_segments % 1000 == 0:
                graphdb.commit(neo4j_edges_transaction)
                neo4j_edges_transaction = graphdb.begin()
                logger.info("Still running. {} relationships completed.".format(nb_segments))
        except KeyError as e:
            logger.warn(str(e))
    
    logger.info("Parsing complete ({} relationships).".format(nb_segments))    
    graphdb.commit(neo4j_edges_transaction)
    cursor_noeuds.close()
    cursor_segments.close() 
    logger.info("Done.")
    