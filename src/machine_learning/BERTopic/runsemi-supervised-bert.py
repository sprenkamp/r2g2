from bertopic import BERTopic
import pandas as pd

# Load your dataset
df_telegram_concat = pd.read_csv(r"C:\Users\rocco\Documents\project0809\r2g2\src\machine_learning\BERTopic\df_telegram_concat.csv", encoding='UTF-8')

# (Non)Sample data
#sample_df = df_telegram_concat.sample(n=20000, random_state=42)
df_data = df_telegram_concat  # Changed the name for clarity since it's not a sample
docs = df_data['text'].tolist()
labels = df_data['cluster_id'].tolist()

# Create BERTopic model with a multilingual sentence transformer model
topic_model = BERTopic(embedding_model="paraphrase-multilingual-MiniLM-L12-v2", verbose=True, nr_topics="auto", min_topic_size=100)

# Train the model
topic_model.fit(docs, y=labels)
topic_words = topic_model.get_topic_info()
print(topic_words)

save_path = r"C:\Users\rocco\Documents\project0809\r2g2\src\machine_learning\bertopic_model.safetensors"  # Added the .safetensors extension

# Save the BERTopic model in .safetensors format
topic_model.save(save_path, save_embedding_model=True)  
