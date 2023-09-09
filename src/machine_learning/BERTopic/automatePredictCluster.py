import argparse
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from bertopic import BERTopic
from pymongo import MongoClient
import pandas as pd
import dateutil
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def get_database_connection():
    ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
    ATLAS_USER = os.environ["ATLAS_USER"]
    cluster = MongoClient("mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))
    return cluster

def validate_database(s):
    database_name, collection_name = s.split('.')
    cluster = get_database_connection()
    db = cluster[database_name]
    list_of_collections = db.list_collection_names()
    if collection_name not in list_of_collections:
        raise Exception("Collection does not exit")
    return s

def get_telegram_data(database_name, collection_name, condition, col_selection):
    telegram_collection = cluster[database_name][collection_name]
    data_telegram = pd.DataFrame(list(telegram_collection.find(condition, col_selection)))
    print("new data len: ", len(data_telegram))
    return data_telegram

def load_model():
    # TODO load model from remote environment
    # read model
    output_folder = "data/telegram/results/test/"
    model = BERTopic.load(f"{output_folder}/BERTopicmodel")
    return model

def get_new_cluster_aggregation(df):
    df['date'] = pd.to_datetime(df['messageDatetime']).dt.strftime('%Y-%m-%d')
    df.drop(['messageText', 'messageDatetime'], axis=1, inplace=True)
    aggregation = df.groupby(['date', 'country', 'state', 'cluster']).value_counts().reset_index(name='count')
    return aggregation

def process_aggregation(data_telegram, model):
    aggregation = pd.DataFrame()

    # judge whether have new data
    if len(data_telegram) > 0:

        predicted_text = data_telegram['messageText'].to_list()

        topics, probs = model.transform(predicted_text)

        data_telegram['cluster'] = topics

        # TODO zhengyuan update topics to database: scrape.telegram

        # TODO zhengyuan, haoxin: give cluster name. currently cluster is 'label'

        # agg data: by date, country, state, cluster
        max_scraping_date_time = data_telegram['messageDatetime'].max()
        aggregation = get_new_cluster_aggregation(data_telegram)
        aggregation[
            'lastMessageTime'] = max_scraping_date_time.isoformat()  # returns a date that satisfies standard ISO
    else:
        # no updated data
        pass

    return aggregation

if __name__ == '__main__':
    """
    python src/machine_learning/BERTopic/automatePredictCluster.py -i scrape.telegram -o test.bertopic_test
    """

    # This code is use to calculate the frequenct of topic
    # (1) fetch previous aggregation calculation
    # (2) fetch telegram data which are new in database
    # (3) calculate topic freqency using bert model. Aggregate by date, country, state, topic
    # (4) combine old agg and new agg together

    # TODO issue description
    #  convert topic label to topic name
    #  update topic name to scrape.telegram


    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_database', help="Specify the input database", type=validate_database, required=True)
    parser.add_argument('-o', '--output_database', help="Specify the output database", required=True)
    args = parser.parse_args()

    i_database_name, i_collection_name = args.input_database.split('.')
    o_database_name, o_collection_name = args.output_database.split('.')

    cluster = get_database_connection()
    telegram_cols_selection = {'_id': 1, 'messageDatetime': 1, 'country': 1, 'state': 1, 'messageText': 1, }

    model = load_model()

    # fetch previous aggregation results
    bert_collection = cluster[o_database_name][o_collection_name]
    data_valuecount = pd.DataFrame(list(bert_collection.find({}, {'_id': 0})))

    if len(data_valuecount) == 0:
        # fetch all data
        condition = {}
        data_telegram = get_telegram_data(i_database_name, i_collection_name, condition, telegram_cols_selection)
        # TODO zhengyuan Only use sample data for testing. Should remove this line in prd env
        data_telegram = data_telegram.sample(frac=.05)
        print('sample data len', len(data_telegram))
        aggregation_new = process_aggregation(data_telegram, model)
    else:
        aggregation_new = pd.DataFrame()
        for index, row in data_valuecount.iterrows():

            max_update_time = row['lastMessageTime']
            country = row['country']
            state = row['state']
            print("[%s] [%s] last update time: [%s]" % (state, country, max_update_time))

            # get data after date threshold
            max_update_time = dateutil.parser.parse(max_update_time)  # converting string to datetime object
            condition = {
                "state": state,
                "country": country,
                "messageDatetime": {"$gt": max_update_time}
            }

            data_telegram = get_telegram_data(i_database_name, i_collection_name, condition, telegram_cols_selection)
            aggregation_by_granularity = process_aggregation(data_telegram, model)
            aggregation_new = pd.concat([aggregation_new, aggregation_by_granularity])

    # concat previous aggregation and new aggregation
    final_data = pd.concat([data_valuecount, aggregation_new])
    final_aggregation = final_data.groupby(['date', 'country', 'state', 'cluster'], as_index=False). \
        agg({'count': 'sum', 'lastMessageTime': 'max'})

    # overwrite aggregation in database
    cluster[o_database_name]['bertopic_copy'].insert_many(final_aggregation.to_dict('records'))
    cluster[o_database_name]['bertopic_copy'].rename(o_collection_name, dropTarget=True)

