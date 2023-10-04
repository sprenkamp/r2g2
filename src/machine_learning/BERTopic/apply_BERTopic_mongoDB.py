import argparse
from pymongo import MongoClient
import pandas as pd
from bertopic import BERTopic
import os
from dotenv import load_dotenv

def predict_and_update(model_path):
    # 1. Connect to MongoDB and fetch the data
    
    # Load .env variables
    load_dotenv('.env')

    # Access variables from .env file
    ATLAS_USER = os.getenv("ATLAS_USER")
    ATLAS_TOKEN = os.getenv("ATLAS_TOKEN")

    client = MongoClient(
        "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(
            ATLAS_USER, ATLAS_TOKEN))

    db = client["test"]
    col = db["telegram"]

    # Query
    query = {
        "$and": [
            {"country": "Switzerland"}
        ]
    }

    # Execute Query
    cursor = col.find(query)

    # 2. Convert MongoDB data to a pandas dataframe
    df = pd.DataFrame(list(cursor))
    
    # Assume the column containing the text data is named 'text'
    texts = df['messageText'].tolist()

    # 3. Load your pre-trained BERTopic model
    topic_model = BERTopic.load(model_path)

    # 4. Predict the class (topic) for each instance
    topics, _ = topic_model.transform(texts)
    df['predicted_class'] = topics

    # 5. Update MongoDB records with the predicted class
    for index, row in df.iterrows():
        col.update_one({"_id": row["_id"]}, {"$set": {"predicted_class": row["predicted_class"]}})

    print("Records updated successfully!")
    
    client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict and update MongoDB records using a pre-trained BERTopic model.')
    parser.add_argument('-m','--model_path', type=str, help='Path to the pre-trained BERTopic model.')

    args = parser.parse_args()
    predict_and_update(args.model_path)
