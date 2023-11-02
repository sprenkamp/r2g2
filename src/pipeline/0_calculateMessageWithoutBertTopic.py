import os
from dotenv import load_dotenv
load_dotenv()
import argparse
from pymongo import MongoClient
import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

import openai
openai.api_key = os.environ["OPENAI_API_KEY"]

def validate_local_file(f):  # function to check if file exists
    if not os.path.exists(f):
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f

def get_chats_list(input_file_path):
    """
    Args:
        input_file_path: chats path

    Returns: pandas dataframe. e.g.
            |country|chat|
            |Switzerland|https://t.me/zurich_hb_help|
            |Switzerland|https://t.me/helpfulinfoforua|
    """
    countries, chats = list(), list()
    with open(input_file_path, 'r') as file:
        for line in file.readlines():
            if line.startswith("#"):
                country = line.replace('#', '').replace('\n', '')
            else:
                chat = line.replace('\n', '')

                chats.append(chat)
                countries.append(country)

    df = pd.DataFrame(list(zip(countries, chats)),
                      columns=['country', 'chat'])
    return df

def calculate_message_without_bert_topic_label(chats, collection):
    '''
    find new coming scraping data. Show how many data should be trained and given topic labels
    Args:
        chats:
        collection:

    '''
    for index, row in chats.iterrows():
        selection_criteria = {
            "$and": [
                {'chat': row['chat']},
                {"topicUpdateDate": {'$exists': False}},
            ],
        }
        projection = {'_id': 1}
        cursor = collection.find(selection_criteria, projection)

        print(len(list(cursor.clone())), "records need to be trained", row['chat'])



if __name__ == '__main__':
    '''
    Add messageDate to the whole collection: scrape.telegram
    use command:
        (1) prd dataset
        python src/pipeline/0_calculateMessageWithoutBertTopic.py \
        -i data/telegram/queries/switzerland_groups.txt \
        -o scrape.telegram

        (2) testing dataset
        python src/pipeline/0_calculateMessageWithoutBertTopic.py \
        -i data/telegram/queries/switzerland_groups.txt \
        -o test.telegram

    '''

    # parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file_path', help="Specify the input file", type=validate_local_file,
                        required=True)
    parser.add_argument('-o', '--output_database', help="Specify the output database", required=True)
    args = parser.parse_args()

    # connect to db
    ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
    ATLAS_USER = os.environ["ATLAS_USER"]
    cluster = MongoClient(
        "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))

    # specify names of database and collection
    db_name, collection_name = args.output_database.split('.')
    collection = cluster[db_name][collection_name]

    chats = get_chats_list(args.input_file_path)

    # operate collection
    calculate_message_without_bert_topic_label(chats, collection)

    cluster.close()