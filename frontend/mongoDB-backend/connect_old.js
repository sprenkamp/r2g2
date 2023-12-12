// scp -i "D:\aws_key\aws_node.pem" "D:\visualstudiocode\project\r2g2\r2g2\frontend\mongoDB-backend\connect.js" ec2-user@ec2-13-48-253-68.eu-north-1.compute.amazonaws.com:/home/ec2-user/

const express = require('express');
const compression = require('compression');
const { MongoClient } = require('mongodb');
// const redis = require('redis');
const app = express();
const dotenv = require("dotenv");
const cors = require("cors")
dotenv.config()
app.use(compression());

const allowedOrigins = [
  'http://localhost:5173',
  'http://13.48.253.68/6379',
  'https://13.48.253.68/6379',
  'http://localhost:6379',
  'https://main--coruscating-alpaca-1de6ac.netlify.app',
  'https://governmentasaplatform.ch',
  'https://www.governmentasaplatform.ch',
  'https://db.governmentasaplatform.ch',
  'www.governmentasaplatform.ch',
  'governmentasaplatform.ch',
  'ELB-r2g2-802525093.eu-north-1.elb.amazonaws.com',
];

app.use(cors({
  origin: function (origin, callback) {
    if (allowedOrigins.indexOf(origin) !== -1 || !origin) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));

app.get('/:databaseName/:collectionName', async (req, res) => {
  const databaseName = req.params.databaseName;
  const collectionName = req.params.collectionName;
  let client;

  try {
    const uri = process.env.MONGO_URL;
    client = new MongoClient(uri);
    await client.connect();
    const database = client.db(databaseName);
    const collection = database.collection(collectionName);
    const query = {predicted_class:{$ne:"Unknown"}};
    const options = {
      projection: { _id: 0, count: 1, messageDate: 1, predicted_class: 1, state: 1, country: 1 },
    };
    const collectionData = await collection.find(query, options).toArray();
    res.json(collectionData);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'An error occurred while fetching data.' });
  } finally {
    if (client) {
      await client.close();
    }
  }
});

// const redisClient = redis.createClient({
//   host: 'localhost',
//   port: 6379,
// });

// app.get('/:databaseName/:collectionName', async (req, res) => {
//   const databaseName = req.params.databaseName;
//   const collectionName = req.params.collectionName;
//   const cacheKey = `${databaseName}:${collectionName}`;

//   redisClient.get(cacheKey, async (err, cachedData) => {
//     if (err) {
//       console.error(err);
//       res.status(500).json({ error: 'An error occurred while fetching data from Redis.' });
//       return;
//     }

//     if (cachedData) {
//       const parsedData = JSON.parse(cachedData);
//       res.json(parsedData);
//     } else {
//       let client;

//       try {
//         const uri = process.env.MONGO_URL;
//         client = new MongoClient(uri);
//         await client.connect();
//         const database = client.db(databaseName);
//         const collection = database.collection(collectionName);
//         const query = { predicted_class: { $ne: "Unknown" } };
//         const options = {
//           projection: { _id: 0, count: 1, messageDate: 1, predicted_class: 1, state: 1, country: 1 },
//         };
//         const collectionData = await collection.find(query, options).toArray();

//         redisClient.setex(cacheKey, 7*24*60*60, JSON.stringify(collectionData));

//         res.json(collectionData);
//       } catch (error) {
//         console.error(error);
//         res.status(500).json({ error: 'An error occurred while fetching data from the database.' });
//       } finally {
//         if (client) {
//           await client.close();
//         }
//       }
//     }
//   });
// });

app.get('/healthz', (req, res) => {
  res.status(200).send('OK');
});

// run serve
const port = process.env.PORT || 8000; // default port 3000
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
