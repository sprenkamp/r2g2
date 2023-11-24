import os
from dotenv import load_dotenv
load_dotenv()
import argparse
from pymongo import MongoClient
import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

def add_end_label(collection):
    '''
    load pretrained bert model and generate topic labeling.
    can adjust batch size to control parallel

    Args:
        collection:

    Returns:

    '''

    # select new coming data and ensure these data have been process completely
    selection_criteria = {
        "topicUpdateDate": {'$exists': False},
        "predicted_class": {'$exists': True},
    }

    from datetime import date
    topicUpdateDate = date.today().strftime("%Y-%m-%d")

    collection.update_many(selection_criteria, {"$set": {"topicUpdateDate": topicUpdateDate}})

if __name__ == '__main__':

    '''
    Add messageDate to the whole collection: scrape.telegram
    use command:
        （1） prd dataset
        python src/pipeline/4_addCompletionLabel.py -o scrape.telegram
        （2） testing dataset
        python src/pipeline/4_addCompletionLabel.py -o test.telegram        
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
    add_end_label(collection)

    cluster.close()