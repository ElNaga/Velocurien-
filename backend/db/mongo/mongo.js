const { MongoClient } = require("mongodb");

class MongoConnector {
  constructor(url, dbName, username, password) {
    this.url = url;
    this.dbName = dbName;
    this.username = username;
    this.password = password;

    this.mongoClient = new MongoClient(this.url);
  }

  async connect() {
    try {
      await this.mongoClient.connect();
      this.db = this.mongoClient.db(this.dbName);
      console.log("Connected to MongoDB");
    } catch (err) {
      console.error("Failed to connect to MongoDB:", err);
      throw err;
    }
  }

  disconnect() {
    this.mongoClient.close();
  }
  isConnected() {
    return this.mongoClient.isConnected();
  }
}
module.exports = MongoConnector;
