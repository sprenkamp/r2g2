from telethon import TelegramClient, events, sync, errors
from telethon.sessions import StringSession
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
import datetime
from tqdm import tqdm
import argparse

from pymongo import MongoClient
from pymongo import collection
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

# connect to db
cluster = MongoClient(
    "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))
db = cluster["scrape"]
collection = db["telegram"]

# set index: these composite indexes can not identify one record specifically
# collection.create_index([("date", -1), ('channel_id'), ('message'), ], unique=True)

def validate_file(f): #function to check if file exists
    if not os.path.exists(f):
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f

async def callAPI(input_file_path):
    """
    This function takes an input file, output folder path
    It reads the input file, extracts the chats and then uses the TelegramClient to scrape message.text and message.date from each chat.
    Appending the chat's URL, message text, and message datetime to different lists.
    Then it creates a dataframe from the lists and saves the dataframe to a CSV file in the specified output folder.

    :input_file_path: .txt file containing the list of chats to scrape, each line should represent one chat
    :output_folder_path: folder path where the output CSV file will be saved containing the scraped data
    """

    data = pd.read_csv(input_file_path, keep_default_na=False)

    for index, row in tqdm(data.iterrows(), total=data.shape[0]):
        country = row['country']
        state = row['state']
        city = row['city']
        chat = row['chat']

        # find max time in the database
        time_col = 'date' # "update_time"
        search_max_date = collection.find_one({"chat": chat}, sort=[(time_col, -1)])
        if search_max_date is None:
            max_time = None
        else:
            # avoid include the record which date is equivalent to max_time_db
            max_time = search_max_date[time_col] + datetime.timedelta(seconds=1)

        print("---*--- {} last {} time:{} ---*--- ".format(chat, time_col, max_time))

        data_list = list()

        async with TelegramClient(StringSession(TELEGRAM_STRING_TOKEN), TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:

            async for message in client.iter_messages(chat, reverse=True, offset_date=max_time):

                if message.message is not None:
                    record = dict()
                    record['chat'] = chat
                    record['channel_id'] = message.peer_id.channel_id
                    record['date'] = message.date
                    record['update_time'] = datetime.datetime.now()
                    record['country'] = country
                    record['state'] = state
                    record['city'] = city
                    record['message'] = message.message
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
                collection.insert_many(data_list)
            else:
                print("no updated records")


if __name__ == '__main__':
    """
    example usage in command line:
    python src/helper/scraping/telegram_tools/scrapeTelegramChannelMessages.py -i data/telegram/queries/DACH.txt
    python src/helper/scraping/telegram_tools/scrapeTelegramChannelMessages.py -i data/telegram/queries/chat_with_country.csv
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', help="Specify the input file", type=validate_file, required=True)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(callAPI(args.input_file))
    loop.close()
