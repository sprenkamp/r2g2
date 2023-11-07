// scp -i "D:\aws_key\aws_node.pem" "D:\visualstudiocode\project\r2g2\r2g2\frontend\mongoDB-backend\connect.js" ec2-user@ec2-51-20-75-190.eu-north-1.compute.amazonaws.com:/home/ec2-user/

const express = require('express');
const compression = require('compression');
const { MongoClient } = require('mongodb');
const app = express();
const dotenv = require("dotenv");
const cors = require("cors")
const https = require("https")
dotenv.config()
app.use(compression());


const allowedOrigins = [
  'http://localhost:5173',
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

  try {
    const uri = process.env.MONGO_URL;
    const client = new MongoClient(uri);
    await client.connect();
    const database = client.db(databaseName);
    const collection = database.collection(collectionName);
    const collectionData = await collection.find().toArray();
    res.json(collectionData);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'An error occurred while fetching data.' });
  } finally {
    client.close();
  }
});

app.get('/healthz', (req, res) => {
  res.status(200).send('OK');
});

// run serve
const port = process.env.PORT || 8000; // default port 3000
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});