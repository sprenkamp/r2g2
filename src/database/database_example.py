import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

# useful links for fetching data from MongoDB
# https://www.w3schools.com/python/python_mongodb_query.asp
# https://www.mongodb.com/docs/manual/reference/method/db.collection.find/

# connect to db
ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
ATLAS_USER = os.environ["ATLAS_USER"]
cluster = MongoClient(
    "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))

# specify names of database and collection
db_name = 'scrape'
collection_name = 'telegram'
collection = cluster[db_name][collection_name]

# fetch data
condition = {'chat': 'https://t.me/helpfulinfoforua'}
selection = {'_id': 0}  # don't select id
query_res = collection.find(condition, selection)  # use find, find_one to perform query
df = pd.DataFrame(list(query_res))

print(df)


############### discard this method to fetch data from database ###############

# The self-design interface might make the whole project complex. Now we use method above to fetch data from database

# from src.database.accessMongoDB import *
# # Function1: load_one_record_from_db(db_name, collection_name, cols)
# # Function2: load_all_record_from_db(db_name, collection_name, cols)
# # get data in pandas dataframe format
#
# db = MongoDB()
# # Example1: one data record+all columns
# # if you want all cols, just write []
# data = db.load_one_record_from_db('scrape', 'telegram', [])
# print(data)
#
# # Example2: all data + specific columns
# data = db.load_all_record_from_db('test', 'employee', ['name', 'email'])
# print(data)

#################################################################################