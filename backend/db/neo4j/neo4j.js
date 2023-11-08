const Neo4jDriver = require('neo4j-driver')

export class Neo4jConnector{
    constructor(url, dbName, username, password){
        this.url = url;
        this.dbName = dbName;
        this.username = username;
        this.password = password;
    }

    connect(){
        Neo4jDriver.driver(url, 
                           neo4j_driver.auth.basic(username, password))
    }

    disconnect(){
        Neo4jDriver.close()
    }
}
