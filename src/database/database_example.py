import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
from src.database.accessMongoDB import *


# Function1: load_one_record_from_db(db_name, collection_name, cols)
# Function2: load_all_record_from_db(db_name, collection_name, cols)
# get data in pandas dataframe format

db = MongoDB()
# Example1: one data record+all columns
# if you want all cols, just write []
data = db.load_one_record_from_db('scrape', 'telegram', [])
print(data)

# Example2: all data + specific columns
data = db.load_all_record_from_db('test', 'employee', ['name', 'email'])
print(data)




