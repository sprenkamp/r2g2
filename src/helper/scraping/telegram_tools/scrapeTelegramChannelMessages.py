from telethon import TelegramClient, events, sync, errors
from telethon.sessions import StringSession
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
import datetime
from tqdm import tqdm
import argparse

from pymongo import MongoClient, errors
import pandas as pd


# To run this code. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

# if you run code locally, you should store variables in .env file.
# If you run code in Github platform, code will fetch secret/variables automatically
TELEGRAM_API_ID = os.environ["TELEGRAM_API_ID"]
TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]
TELEGRAM_STRING_TOKEN = os.environ["TELEGRAM_STRING_TOKEN"]
ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
ATLAS_USER = os.environ["ATLAS_USER"]


def validate_local_file(f): #function to check if file exists
    if not os.path.exists(f):
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f

def initialize_database(database_name, collection_name):
    '''
    use names of database and collection to fetch specific collection
    Args:
        database_name:
        collection_name:

    Returns:

    '''
    cluster = MongoClient("mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))
    collection = cluster[database_name][collection_name]
    return collection

async def callAPI():
    """
    This function takes an input file, output folder path
    It reads the input file, extracts the chats and then uses the TelegramClient to scrape message.text and message.date from each chat.
    Appending the chat's URL, message text, and message datetime to different lists.
    Then it creates a dataframe from the lists and saves the dataframe to a CSV file in the specified output folder.

    :input_file_path: .txt file containing the list of chats to scrape, each line should represent one chat
    :output_folder_path: folder path where the output CSV file will be saved containing the scraped data
    """

    # # Option 1: read from local file
    # data = pd.read_csv(input_file_path, keep_default_na=False)

    # Option 2: read from Mongodb
    query_res = input_collection.find({}, {'_id': 0})  # use find, find_one to perform query
    data = pd.DataFrame(list(query_res))

    print(len(data))

    for index, row in tqdm(data.iterrows(), total=data.shape[0]):

        async with TelegramClient(StringSession(TELEGRAM_STRING_TOKEN), TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
            country = row['country']
            state = row['state']
            city = row['city']
            chat = row['chat']

            # find max time in the database
            time_col = 'messageDatetime'  # "update_time"
            search_max_date = output_collection.find_one({"chat": chat}, sort=[(time_col, -1)])
            if search_max_date is None:
                max_time = None
            else:
                # avoid include the record which date is equivalent to max_time_db
                max_time = search_max_date[time_col] + datetime.timedelta(seconds=1)

            print("{} last {} time: {} ".format(chat, time_col, max_time))

            data_list = list()

            async for message in client.iter_messages(chat, reverse=True, offset_date=max_time):

                if message.message is not None:
                    record = dict()
                    record['chat'] = chat
                    record['channel_id'] = message.peer_id.channel_id
                    record['messageDatetime'] = message.date
                    record['update_time'] = datetime.datetime.now()
                    record['country'] = country
                    record['state'] = state
                    record['city'] = city
                    record['messageText'] = message.message
                    record['views'] = message.views if message.views is not None else 0
                    record['forwards'] = message.forwards if message.forwards is not None else 0

                    if message.replies is None:
                        record['replies'] = 0
                    else:
                        record['replies'] = message.replies.replies

                    if message.reactions is None:
                        record['reactions'] = []
                    else:
                        reaction = dict()
                        for i in message.reactions.results:
                            try:
                                reaction[i.reaction.emoticon] = i.count
                            except:
                                # same message don't have emotion labels (reaction.emoticon)
                                pass
                        record['reactions'] = reaction

                    data_list.append(record)

            print("data len:{}".format(len(data_list)))

            if len(data_list) > 0:
                output_collection.insert_many(data_list)
            else:
                print("no updated records")


def validate_database(s):
    database_name, collection_name = s.split('.')
    cluster = MongoClient("mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))
    db = cluster[database_name]
    list_of_collections = db.list_collection_names()
    if collection_name not in list_of_collections:
        raise Exception("Collection does not exit")
    return s

if __name__ == '__main__':
    """
    example usage in command line:
    
    Option 1: read chats from local file
    python src/helper/scraping/telegram_tools/scrapeTelegramChannelMessages.py -i data/telegram/queries/chat_with_country.csv -o scrape.telegram
    
    Option 2: read chats from MongoDB
    python src/helper/scraping/telegram_tools/scrapeTelegramChannelMessages.py -i scrape.telegramChatsWithState -o scrape.telegram
    """

    # # Option 1: read from local file
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-i', '--input_file_path', help="Specify the input file", type=validate_local_file, required=True)
    # parser.add_argument('-o', '--output_database', help="Specify the output database", required=True)
    # args = parser.parse_args()
    #
    # o_database_name, o_collection_name = args.output_database.split('.')
    # output_collection = initialize_database(o_database_name, o_collection_name)
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(callAPI(args.input_file_path))
    # loop.close()


    # Option 2: read from MongoDB
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_database', help="Specify the input database", type=validate_database, required=True)
    parser.add_argument('-o', '--output_database', help="Specify the output database", required=True)
    args = parser.parse_args()

    i_database_name, i_collection_name = args.input_database.split('.')
    o_database_name, o_collection_name = args.output_database.split('.')
    input_collection = initialize_database(i_database_name, i_collection_name)
    output_collection = initialize_database(o_database_name, o_collection_name)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(callAPI())
    loop.close()
