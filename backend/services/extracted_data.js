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

module.exports = {
  initialize,
  getExtractedData,
};
