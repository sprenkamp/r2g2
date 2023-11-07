# TODO update aggregate.TelegramCount

import os
from pymongo import MongoClient
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Aggregate messageDate and predicted_class to update TelegramCount.")
parser.add_argument('-o', '--output_database', required=True, help="Specify the output database and collection in the format 'database.collection'")
args = parser.parse_args()

# Extract the database and collection names from the provided argument
db_name, collection_name = args.output_database.split('.')

# Load environment variables
ATLAS_TOKEN = os.getenv("ATLAS_TOKEN")
ATLAS_USER = os.getenv("ATLAS_USER")

# Connect to MongoDB
cluster = MongoClient(f"mongodb+srv://{ATLAS_USER}:{ATLAS_TOKEN}@cluster0.mongodb.net/")
collection = cluster[db_name][collection_name]

# Aggregate to count the predicted_class occurrences by messageDate
pipeline = [
    {
        '$match': {
            'TelegramCount': {'$exists': False}  # Filter to consider only documents without TelegramCount
        }
    },
    {
        '$group': {
            '_id': {
                'messageDate': '$messageDate',
                'predicted_class': '$predicted_class'
            },
            'TelegramCount': {'$sum': 1}  # Count the occurrences
        }
    }
]

# Execute the aggregation pipeline
results = list(collection.aggregate(pipeline))

# Update the documents with the new TelegramCount
for result in results:
    collection.update_many(
        {
            'messageDate': result['_id']['messageDate'],
            'predicted_class': result['_id']['predicted_class'],
            'TelegramCount': {'$exists': False}
        },
        {
            '$set': {'TelegramCount': result['TelegramCount']}
        }
    )
