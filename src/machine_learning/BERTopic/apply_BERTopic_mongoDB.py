from pymongo import MongoClient, UpdateOne
import pandas as pd
from bertopic import BERTopic
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def fetch_data():
    global col
    load_dotenv('.env')
    ATLAS_USER = os.getenv("ATLAS_USER")
    ATLAS_TOKEN = os.getenv("ATLAS_TOKEN")
    client = MongoClient("mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))
    db = client["scrape"]
    col = db["telegram"]
    query = {"$and": [{"country": "Switzerland"}]}
    cursor = col.find(query)
    df = pd.DataFrame(list(cursor))
    return df, client  # Return the client as well

def predict_topics(df, model_path):
    texts = df['messageText'].tolist()
    topic_model = BERTopic.load(model_path)
    topics, _ = topic_model.transform(texts)
    df['predicted_class'] = topics
    return df

def update_chunk(chunk):
    bulk_operations = [UpdateOne({"_id": row["_id"]}, {"$set": {"predicted_class": row["predicted_class"]}}) for index, row in chunk.iterrows()]
    col.bulk_write(bulk_operations)

def predict_and_update(model_path):
    df, client = fetch_data()  # Get the client as well
    print("data loaded")
    print(df.shape)
    # df = df[:3000]
    df = predict_topics(df, model_path)
    print("topics predicted")

    # Splitting dataframe into chunks of 1000
    chunks = [df.iloc[i:i+1000] for i in range(0, len(df), 1000)]

    # Using ThreadPoolExecutor to update chunks in parallel
    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(update_chunk, chunks), total=len(chunks)))

    print("Records updated successfully!")
    
    client.close()  # Close the client here after all operations are done

# Example usage
model_path = "kdot/BERTopicTelegramAnalysis"
predict_and_update(model_path)
