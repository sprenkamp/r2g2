import os
from dotenv import load_dotenv

load_dotenv()
from pymongo import MongoClient
import argparse

'''
Add messageDate to the whole collection: scrape.telegram
use command:
    (1) prd
    python src/pipeline/2_updateTopicFrequencyCount.py -i scrape.telegram -o aggregate.TelegramCount

    (2)test
    python src/pipeline/2_updateTopicFrequencyCount.py -i test.telegram -o test.TelegramCount
'''

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Aggregate messageDate, predicted_class, state, and country to update count.")
parser.add_argument('-i', '--input_database', required=True,
                    help="Specify the input database and collection in the format 'database.collection'")
parser.add_argument('-o', '--output_database', required=True,
                    help="Specify the output database and collection in the format 'database.collection'")
args = parser.parse_args()

# Extract the database and collection names from the provided argument
i_db_name, i_collection_name = args.input_database.split('.')
o_db_name, o_collection_name = args.output_database.split('.')

# Load environment variables
ATLAS_TOKEN = os.getenv("ATLAS_TOKEN")
ATLAS_USER = os.getenv("ATLAS_USER")

# Connect to MongoDB
cluster = MongoClient("mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))
collection = cluster[i_db_name][i_collection_name]

# Aggregate to count the occurrences of predicted_class for each combination of messageDate, state, and country
pipeline = [
    {
        '$match': {
            "messageDate": {'$exists': True},
            "predicted_class": {'$exists': True},
            "state": {'$exists': True},
            "country": {'$exists': True},
        }
    },
    {
        '$group': {
            '_id': {
                'messageDate': '$messageDate',
                'predicted_class': '$predicted_class',
                'state': '$state',
                'country': '$country'
            },
            'count': {'$sum': 1}  # Count the occurrences
        }
    },
    {
        '$project': {
            'messageDate': '$_id.messageDate',
            'predicted_class': '$_id.predicted_class',
            'state': '$_id.state',
            'country': '$_id.country',
            '_id': {
                # to make the _id take less space: compact all keys together
                '$concat': [
                    '$_id.messageDate', '-', '$_id.predicted_class', '-', '$_id.state', '-', '$_id.country'
                ]
            },
            'count': 1
        }
    },
    {
        '$merge': {
            "into": {"db": o_db_name, "coll": o_collection_name},
            "on": "_id",
            "whenMatched": "replace",
            "whenNotMatched": "insert"
        }
    }
]

collection.aggregate(pipeline)

cluster.close()