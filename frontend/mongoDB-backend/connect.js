const express = require('express');
const compression = require('compression');
const { MongoClient } = require('mongodb');
const app = express();
const dotenv = require("dotenv");
const cors = require("cors")
dotenv.config()
app.use(cors());
app.use(compression());

app.get('/:databaseName/:collectionName', async (req, res) => {
  const databaseName = req.params.databaseName;
  const collectionName = req.params.collectionName;

  try {
    const uri = process.env.MONGO_URL;
    const client = new MongoClient(uri);
    await client.connect();

    const database = client.db(databaseName);
    const collection = database.collection(collectionName);

    const collectionData = await collection.find().toArray();

    await client.close();

    res.json(collectionData);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'An error occurred while fetching data.' });
  }
});

// run serve
const port = process.env.PORT || 8000; // default port 3000
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
