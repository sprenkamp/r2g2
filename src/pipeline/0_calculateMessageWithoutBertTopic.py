import os
from dotenv import load_dotenv
load_dotenv()
import argparse
from pymongo import MongoClient
import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

def calculate_message_without_bert_topic_label(collection):
    '''
    find new coming scraping data. Show how many data should be trained and given topic labels
    Args:
        chats:
        collection:

    '''
    pipeline = [
        {
            '$match': {
                "topicUpdateDate": {'$exists': False},
            }
        },
        {
            '$group': {
                '_id': '$chat',
                '#data need bert topic': {'$sum': 1}
            }
        },
    ]
    res = collection.aggregate(pipeline)

    print('--**-- Message need topic label --**--')
    df = pd.DataFrame(list(res))
    print(df)

if __name__ == '__main__':
    '''
    Add messageDate to the whole collection: scrape.telegram
    use command:
        (1) prd dataset
        python src/pipeline/0_calculateMessageWithoutBertTopic.py -i scrape.telegram

        (2) testing dataset
        python src/pipeline/0_calculateMessageWithoutBertTopic.py -i test.telegram

    '''

    # parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_database', help="Specify the input database", required=True)
    args = parser.parse_args()

    # connect to db
    ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
    ATLAS_USER = os.environ["ATLAS_USER"]
    cluster = MongoClient(
        "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))

    # specify names of database and collection
    db_name, collection_name = args.input_database.split('.')
    collection = cluster[db_name][collection_name]

    # operate collection
    calculate_message_without_bert_topic_label(collection)

    cluster.close()