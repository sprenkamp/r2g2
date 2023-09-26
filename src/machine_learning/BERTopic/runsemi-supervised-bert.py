import os
import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from stoppingword_process import stopWords
from cuml.cluster import HDBSCAN
from cuml.manifold import UMAP

class OurBERTopicModel:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def fit_model(self, docs, labels):
        umap_model = UMAP(n_neighbors=25, n_components=10, metric='cosine', low_memory=False, random_state=42)
        hdbscan_model = HDBSCAN(min_cluster_size=100, metric='euclidean', prediction_data=True)
        vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words=stopWords)
        self.model = BERTopic(embedding_model="paraphrase-multilingual-MiniLM-L12-v2", 
                              language="multilingual",
                              verbose=True, 
                              nr_topics="auto",
                              umap_model=umap_model, 
                              hdbscan_model=hdbscan_model,
                              vectorizer_model=vectorizer_model) 
        self.model.fit(docs, y=labels)
        self.save_results()
        self.write_representative_docs_df()
        
    def save_results(self):
        fig = self.model.visualize_topics()
        fig.write_html(f"{self.output_folder}/bert_topic_model_distance_model.html")
        fig = self.model.visualize_hierarchy()
        fig.write_html(f"{self.output_folder}/bert_topic_model_hierarchical_clustering.html")
        fig = self.model.visualize_barchart(top_n_topics=30)
        fig.write_html(f"{self.output_folder}/bert_topic_model_word_scores.html")
        fig = self.model.visualize_heatmap()
        fig.write_html(f"{self.output_folder}/bert_topic_model_word_heatmap.html")
        self.model.save(f"{self.output_folder}/BERTopicmodel")
        
    def write_representative_docs_df(self):
        writer = pd.ExcelWriter(f"{self.output_folder}/representative_docs.xlsx", engine='xlsxwriter')
        for i in self.model.get_representative_docs().keys():
            df = pd.DataFrame(self.model.get_representative_docs()[i], columns=['message'])
            df.to_excel(writer, sheet_name=self.model.get_topic_info()[self.model.get_topic_info()['Topic'] == i]['Name'].values[0][:31])
        writer.save()
        self.model.get_topic_info().to_csv(f"{self.output_folder}/topic_info.csv")

if __name__ == "__main__":
    df_telegram_concat = pd.read_csv("src/machine_learning/BERTopic/df_telegram_concat.csv", encoding='UTF-8')
    docs = df_telegram_concat['text'].tolist()
    labels = df_telegram_concat['cluster_id'].tolist()
    
    output_folder = "src/machine_learning/BERTopic/Result"
    bertopic_model = OurBERTopicModel(output_folder)
    bertopic_model.fit_model(docs, labels)
