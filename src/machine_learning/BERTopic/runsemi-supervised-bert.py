from bertopic import BERTopic
import pandas as pd

# Load your dataset
df_telegram_concat = pd.read_csv(r"C:\Users\rocco\Documents\project0809\r2g2\src\machine_learning\BERTopic\df_telegram_concat.csv", encoding='ISO-8859-1')

# Sample data
sample_df = df_telegram_concat.sample(n=500, random_state=42)
sample_docs = sample_df['text'].tolist()
sample_y = sample_df['cluster_id'].tolist()

# Create BERTopic model with a multilingual sentence transformer model
topic_model_sample = BERTopic(embedding_model="distiluse-base-multilingual-cased", verbose=True)

# Train the model
topic_model_sample.fit(sample_docs, y=sample_y)
sample_topic_words = topic_model_sample.get_topic_info()
print(sample_topic_words)

save_path = "C:\\Users\\rocco\\Documents\\project0809\\r2g2\\src\\machine_learning\\bertopic_model"

# Save the entire BERTopic model
topic_model_sample.save(save_path, save_embedding_model=True)
