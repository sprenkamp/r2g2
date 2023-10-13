#pip install safetensors
from huggingface_hub import login
from bertopic import BERTopic
import pandas as pd

access_token_write = "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"
login(token = access_token_write)

topic_model = BERTopic.load(r"src\machine_learning\BERTopic\Result_ulti")

# Push to HuggingFace Hub
topic_model.push_to_hf_hub(
    repo_id="Alprocco/Bert_Ukr_in_Swiss",
    save_ctfidf=True,
    serialization='safetensors',
    save_embedding_model='paraphrase-multilingual-MiniLM-L12-v2'
)

df = pd.read_csv(r"src\machine_learning\267clusters_revised_encoded.csv", encoding='utf-8')

# Output the dictionary
output_dict = {}
for index, row in df.iterrows():
    topic = row['Topic']
    cluster_id = row['cluster_id']
    cluster_name = row['cluster_name']
    sub_cluster = row['sub_cluster']
    output_dict[topic] = {'cluster_id': cluster_id, 'cluster_name': cluster_name, 'sub_cluster': sub_cluster}

print(output_dict)
