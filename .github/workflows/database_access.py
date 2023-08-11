import os
from dotenv import load_dotenv
load_dotenv()
import datetime

ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
ATLAS_USER = os.environ["ATLAS_USER"]

import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))

# ######### insert
db = cluster["test"]
collection = db["employee"]

# collection.create_index([("name"), ("date", -1)], unique=True)
post1 = {"name": "amarjx", "email": "amar@mail.com", "date": datetime.datetime.strptime("2023-06-01 00:02:03", '%Y-%m-%d %H:%M:%S')}
post2 = {"name": "Toms", "email": "amar12@mail.com", "date": datetime.datetime.strptime("2023-07-31 00:02:03", '%Y-%m-%d %H:%M:%S')}
post3 = {"name": "Toms", "email": "amar12@mail.com", "date": datetime.datetime.strptime("2023-02-03 00:02:03", '%Y-%m-%d %H:%M:%S')}
post4 = {"name": "Toms", "email": "amar12@mail.com", "date": datetime.datetime.strptime("2023-02-03 00:02:03", '%Y-%m-%d %H:%M:%S')}
collection.insert_many([post1, post2, post3, post4])
print(collection.find())