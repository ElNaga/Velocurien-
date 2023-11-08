let db;

function initialize(database) {
  db = database;
}

async function getRestaurantCount() {
  const collection = db.collection("restaurants_raw");
  return await collection.countDocuments({});
}

async function getSegmentCount() {
  const [cyclableCount, routesCount] = await Promise.all([
    db.collection("cyclable_raw").countDocuments({}),
    db.collection("routes_raw").countDocuments({}),
  ]);

  return cyclableCount + routesCount;
}

async function getExtractedData(req, res) {
  try {
    const nbRestaurants = await getRestaurantCount();
    const nbSegments = await getSegmentCount();

    res.status(200).send({
      nbRestaurants,
      nbSegments,
    });
  } catch (err) {
    res.status(500).send({ error: "Failed to retrieve data" });
  }
}

async function transformData(req, res) {
  try {
    // Assuming the collection name is 'cyclable_raw' or 'routes_raw' or whatever your actual collection is.
    const collection = db.collection("cyclable_raw");

    const restaurantsRawArray = await db.collection('restaurants_raw').find().toArray();

  // Initialize an empty object to store the counts
  const restaurants = {};
  restaurantsRawArray.forEach(document => {
    const type = document.properties.type;
    const count = restaurants[type] || 0; 
    restaurants[type] = count + 1; 
  });

    const aggregateDocumentsCyclableRaw = {
      $group: {
        _id: null, // This will group all documents together
        totalLongueur: {
          $sum: "$properties.LONGUEUR"
        }
      }
    };

    const pipeline = [aggregateDocumentsCyclableRaw];
    const aggregatedResult = await collection.aggregate(pipeline).toArray();

    const totalLongueur = aggregatedResult.length > 0 ? aggregatedResult[0].totalLongueur : 0; // This check is to ensure that you are not trying to access empty array

    res.status(200).send({
      restaurants,
      totalLongueur,
    });
  } catch (err) {
    console.error(err); // More detailed logging
    res.status(500).send({ error: "Failed to retrieve data", message: err.message });
  }
}

module.exports = {
  initialize,
  getExtractedData,
  transformData,
};
