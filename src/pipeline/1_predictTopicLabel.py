import os
from dotenv import load_dotenv
load_dotenv()
import argparse
from pymongo import MongoClient
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
import pandas as pd
import datetime
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

import openai
openai.api_key = os.environ["OPENAI_API_KEY"]

def add_topic_label(collection):
    '''
    load pretrained bert model and generate topic labeling.
    can adjust batch size to control parallel

    Args:
        collection:

    Returns:

    '''

    import bson

    batch_size = 1000

    selection_criteria = {
        "topicUpdateDate": {'$exists': False},
    }
    projection = {'_id': 1,  'messageText': 1}
    cursor = collection.find_raw_batches(selection_criteria, projection, batch_size=batch_size)

    # Iterate through the cursor in batches
    for batch in cursor:
        data = bson.decode_all(batch)
        df = pd.DataFrame(list(data))

        # TODO give topic label to messages in batch

if __name__ == '__main__':

    '''
    Add messageDate to the whole collection: scrape.telegram
    use command:
        （1） prd dataset
        python src/pipeline/1_predictTopicLabel.py -o scrape.telegram
        （2） testing dataset
        python src/pipeline/1_predictTopicLabel.py -o test.telegram        
    '''

    # parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_database', help="Specify the output database", required=True)
    args = parser.parse_args()

    # connect to db
    ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
    ATLAS_USER = os.environ["ATLAS_USER"]
    cluster = MongoClient(
        "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))
    db_name, collection_name = args.output_database.split('.')
    collection = cluster[db_name][collection_name]

    # update embedding for new coming data
    add_topic_label(collection)

    cluster.close()