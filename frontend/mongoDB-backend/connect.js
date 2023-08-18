
// const { MongoClient, ServerApiVersion } = require('mongodb');
// async function main(){
//   /**
//    * Connection URI. Update <username>, <password>, and <your-cluster-url> to reflect your cluster.
//    * See https://docs.mongodb.com/ecosystem/drivers/node/ for more details
//    */
//   const uri = "mongodb+srv://jiayu1922:84BeNhuVyVRUWd5@cluster0.9u0db2l.mongodb.net/?retryWrites=true&w=majority";
//   const client = new MongoClient(uri);

//   try {
//       // Connect to the MongoDB cluster
//       await client.connect();

//       // Make the appropriate DB calls
//       await  listDatabases(client);

//   } catch (e) {
//       console.error(e);
//   } finally {
//       await client.close();
//   }
// }

// main().catch(console.error);


// async function listDatabases(client){
//   databasesList = await client.db().admin().listDatabases();

//   console.log("Databases:");
//   databasesList.databases.forEach(db => console.log(` - ${db.name}`));
// };

const express = require('express');
const { MongoClient } = require('mongodb');
const app = express();
const dotenv = require("dotenv");
const cors = require("cors")
dotenv.config()
app.use(cors());

app.get('/:databaseName/:collectionName', async (req, res) => {
  const databaseName = req.params.databaseName;
  const collectionName = req.params.collectionName;

  try {
    // const uri = "mongodb+srv://refugeeukraineai_test:FKFSPyoomgVAkufs@cluster0.fcobsyq.mongodb.net/";
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
