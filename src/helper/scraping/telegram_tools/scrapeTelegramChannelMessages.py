from telethon import TelegramClient, events, sync
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


# To run this code. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

# if you run code locally, you should store variables in .env file.
# If you run code in Github platform, code will fetch secret/variables automatically
TELEGRAM_API_ID = os.environ["TELEGRAM_API_ID"]
TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]
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

    with open(input_file_path) as file:
        chats = file.readlines()
        chats = [chat.replace('\n','') for chat in chats if not chat.startswith("#")]

    for chat in tqdm(chats):

        async with TelegramClient('SessionName', TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
            # chat_short=chat.split('/')[-1]

            # find max time in the database
            search_max_date = collection.find_one({"chat": chat}, sort=[("update_time", -1)])
            if search_max_date is None:
                max_time = None
            else:
                # avoid include the record which date is equivalent to max_time_db
                max_time = search_max_date['update_time'] + datetime.timedelta(seconds=1)

            print("{} last update time:{}".format(chat, max_time))

            # update time
            update_time = datetime.datetime.now()

            data_list = list()

            async for message in client.iter_messages(chat, reverse=True, offset_date=max_time):
                # print(message)

                record = dict()
                record['chat'] = chat
                record['channel_id'] = message.peer_id.channel_id
                record['messageDatetime'] = message.date
                record['update_time'] = update_time
                record['messageText'] = message.message if message.message is not None else ''

                data_list.append(record)

            print("data len:{}".format(len(data_list)))

            if len(data_list) > 0:
                collection.insert_many(data_list)
            else:
                print("no updated records")

def main():
    """
    example usage in command line:
    python src/helper/scraping/telegram_tools/scrapeTelegramChannelMessages.py -i data/telegram/queries/DACH.txt
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', help="Specify the input file", type=validate_file, required=True)
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(callAPI(args.input_file))
    loop.close()

if __name__ == '__main__':
    main()
