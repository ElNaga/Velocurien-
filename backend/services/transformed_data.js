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

async function getRestaurantData() {
    const cursor = db.collection("restaurants_raw").find({});
    const restaurantData = await cursor.toArray(); // This returns a promise that resolves to an array of documents
    
    return restaurantData;
}

async function calculateSum(req, res) {
  try {
    const cursor = await getRestaurantData();
    // Since we are now dealing with a cursor, we need to use it to iterate over documents or convert it to an array.
    // If you need to perform aggregation, you need to access the collection directly, not through the cursor.
    const collection = db.collection("restaurants_raw"); // You need to ensure 'db' is defined in this context

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

    const totalLongueur = aggregatedResult.length > 0 ? aggregatedResult[0].totalLongueur : 999; // This check is to ensure that you are not trying to access empty array

    res.status(200).send({
      totalLongueur,
      'ok':'ok',
    });
  } catch (err) {
    console.error(err); // More detailed logging
    res.status(500).send({ error: "Failed to retrieve data", message: err.message });
  }
}

module.exports = {
  initialize,
  getExtractedData,
  calculateSum,
};
