const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const MongoConnector = require("./db/mongo/mongo.js");

const heartbeat = require("./services/heartbeat.js");
const extractedData = require("./services/extracted_data.js");

const port = 3000;

const corsOptions = {
  origin: "*",
  methods: ["GET", "PUT", "POST", "PATCH", "DELETE", "UPDATE"],
  credentials: true,
};

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cors(corsOptions));

const mongoConnector = new MongoConnector(
  "mongodb://mongo:27017/velocurien",
  "velocurien",
  "",
  ""
);

mongoConnector
  .connect()
  .then(async () => {
    const fs = require("fs");

    async function insertDataIfCollectionEmpty(filePath, collectionName) {
      const fileData = fs.readFileSync(filePath, "utf8");
      const parsedData = JSON.parse(fileData);
      const documentsToInsert = parsedData.features || [parsedData];

      const collection = mongoConnector.db.collection(collectionName);
      const count = await collection.countDocuments({});

      if (count === 0) {
        collection.insertMany(documentsToInsert, (insertErr, res) => {
          if (insertErr) throw insertErr;
          console.log(
            `Inserted into ${collectionName}: ${res.insertedCount} rows`
          );
        });
      } else {
        console.log(`${collectionName} is not empty. Skipping data insertion.`);
      }
    }

    await insertDataIfCollectionEmpty(
      "./data_raw/businesses.geojson",
      "restaurants_raw"
    );
    await insertDataIfCollectionEmpty(
      "./data_raw/reseau_cyclable.geojson",
      "cyclable_raw"
    );
    await insertDataIfCollectionEmpty("./data_raw/routes.json", "routes_raw");

    extractedData.initialize(mongoConnector.db);

    app.get("/heartbeat", heartbeat.getHeartbeat);
    app.get("/extracted_data", extractedData.getExtractedData);
    app.get("/transformed_data", extractedData.transformData);

    app.listen(port, () => {
      console.log(`App is listening at http://localhost:${port}`);
    });
  })
  .catch((err) => {
    console.error("Failed to connect to MongoDB", err);
    process.exit(1); // Exit the process with an error code
  });

// Handle shutdown signals (e.g., CTRL+C)
process.on("SIGINT", () => {
  console.log("Gracefully shutting down...");
  mongoConnector.disconnect();
  process.exit();
});
