# VÉLOCURIEN 

## Phase 2 : Dérisquer l'application

### Conteneurs Docker
Les conteneurs suivants sont lancés lors de l'éxécution de Docker Compose :
* *backend* : Contient le serveur web permettant l'accès à l'API REST en utilisant Express sur Node.
* *mongo* : Contient le moteur de base de données MongoDB (version 7.0)
* *neo4j* : Contient le moteur de base de données Neo4J (version 5.12)

En plus, un profil *staging* est également disponible:
* *stagingservice* : Contient un environnement Python qui charge les données dans l'environnement de staging.
* *stagingdb* : Base de données MongoDB possédant les données brutes importées à partir des fichiers JSON de la Ville de Montréal.

Le conteneur *frontend* est inactif par défaut pour cette phase du projet. Il contient une installation de Vue3 sur Node.

#### Environnement staging
Pour lancer l'environnement de staging, en plus du backend, utiliser la commande ```docker-compose --profile staging up```.

Le conteneur "stagingservice" (Python) ajoutera les données dans la base de données de staging et s'arrêtera, laissant seulement la base de données active.

La base de données de staging est accessible sur le port 27018.


## Phase 1 : Étude de faisabilité

### Conteneurs Docker

Les conteneurs suivants sont lancés lors de l'éxécution de Docker Compose :
* *backend* : Contient le serveur web permettant l'accès à l'API REST en utilisant Express sur Node.
* *mongo* : Contient le moteur de base de données MongoDB (version 7.0)
* *neo4j* : Contient le moteur de base de données Neo4J (version 5.12)

Le conteneur *frontend* est inactif par défaut pour cette phase du projet. Il contient une installation de Vue3 sur Node.

### Fonctionnalités

L’application répond à la requête @GET /heartbeat sur le port 80.

### Fichiers et répertoires
```
├── backend : API de l'application. Code exécuté par le conteneur "backend".
│   ├── services : Contient les fonctions de l'API.
│   ├── Dockerfile
│   ├── app.js : Application principale.
├── frontend : Interface graphique de l'application. Code exécuté par le conteneur "frontend"
│   ├── src : Sources de l'application.
│   ├── Dockerfile
└── docker-compose.yml : Script Docker Compose
└── README.md
```
