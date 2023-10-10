import os
import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

# Run prompt: pip install xlsxwriter --user
# from cuml.cluster import HDBSCAN 
# from cuml.manifold import UMAP 

# Use cuml to import HDBSCAN and UMAP instead of 'from umap import UMAP' and 'from hdbscan import HDBSCAN' if gpu is applied
# Here are the general steps to install cuml:
# Installation of Miniconda/Anaconda:
#   If you don't have Anaconda or Miniconda installed, install Miniconda to manage environments. Miniconda is a lightweight version:
#   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
#   bash Miniconda3-latest-Linux-x86_64.sh
#   Next, create a new RAPIDS environment: https://docs.rapids.ai/install, then activate by: conda activate rapids-env
#   Now, you can import cuml package: pip install cuml

from umap import UMAP 
from hdbscan import HDBSCAN
import numpy as np
from bertopic.vectorizers import ClassTfidfTransformer
import nltk
from nltk.corpus import stopwords

# Download required NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize an empty list to hold the stopwords
# Warning: removing stop words as a preprocessing step is not advised as the transformer-based embedding models that we use need the full context to create accurate embeddings.
# Instead, we can use the CountVectorizer to preprocess our documents after having generated embeddings and clustered our documents.  ref: https://maartengr.github.io/BERTopic/faq.html#how-do-i-reduce-topic-outliers
stopWords = []

# Define and extend the stopwords list
languages = ['english', 'german', 'french', 'italian', 'russian']
for lang in languages:
    stopWords.extend(stopwords.words(lang)) 

# Adding Ukrainian stopword, need to modify the path of stopwords
with open("data/stopwords/stopwords_ua.txt", encoding='utf-8') as file:
    ukrstopWords = [line.rstrip() for line in file] 
    stopWords.extend(ukrstopWords) 

class OurBERTopicModel:
    """
    This class encapsulates the process of fitting a BERTopic model, visualizing the results, 
    and saving the representative documents and model to disk.
    """
    def __init__(self, output_folder):
        self.output_folder = output_folder
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def fit_model(self, docs, labels): 
        """
        UMAP is used for dimension reduction
        - n_neighbors: This parameter specifies the number of neighboring data points utilized to approximate the local manifold structure. Increase it if too many clusters. 
        Note: set n_neighbors too high will greatly increase the computational pressure.
        - n_components: The number of dimensions we want our data to be reduced to. 
        - metric: The distance metric to use to calculate distance in the high dimensional space. Here, cosine metric is used which measures the cosine of the angle between two vectors.
        - low_memory: Set low_memory to True when instantiating BERTopic. This may prevent blowing up the memory in UMAP
        - random_state: Ensures reproducibility. 

        HDBSCAN is a clustering algorithm.
        min_cluster_size: Minimum number of samples in a cluster for it to be considered a cluster. Here, any cluster with fewer than 200 data points is considered noise.
        metric: The metric used for clustering. euclidean metric calculates the traditional straight-line distance between two points.
        prediction_data: When set to True, additional data is stored to allow predicting cluster assignments for new data.
        
        CountVectorizer
        ngram_range: This defines the minimum and maximum size of word sequences you want to consider. (1, 2) means you're considering both single words and two-word phrases.
        stop_words: These are words like 'and', 'the', 'is', etc. that might not contain important significance to be used in the model.
        min_df: min_df=10 indicates that a word must appear in at least 10 documents unless regarding as stopwords.
        """
        #
        umap_model = UMAP(n_neighbors=20, n_components=15, metric='cosine', low_memory=True, random_state=42)
        hdbscan_model = HDBSCAN(min_cluster_size=100, metric='euclidean', prediction_data=True)
        vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words=list(stopWords), min_df=15)
        # ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
        self.model = BERTopic(embedding_model="paraphrase-multilingual-MiniLM-L12-v2", 
                              language="multilingual",
                              verbose=True,   # Enables detailed logging or output during model training.
                              nr_topics='auto',   # Defines the number of topics the model should extract from the dataset. Can also set to 'auto'.
                              umap_model=umap_model, 
                              hdbscan_model=hdbscan_model,
                              vectorizer_model=vectorizer_model,
                            #   ctfidf_model=ctfidf_model,
                              calculate_probabilities=False
                              )
        self.model.fit(docs, y=labels)
        self.save_results()
        self.write_representative_docs_df()
        
    def save_results(self):
        fig = self.model.visualize_topics()
        fig.write_html(f"{self.output_folder}/bert_topic_model_distance_model.html")
        fig = self.model.visualize_hierarchy()
        fig.write_html(f"{self.output_folder}/bert_topic_model_hierarchical_clustering.html")
        fig = self.model.visualize_barchart(top_n_topics=25)
        fig.write_html(f"{self.output_folder}/bert_topic_model_word_scores.html")
        fig = self.model.visualize_heatmap()
        fig.write_html(f"{self.output_folder}/bert_topic_model_word_heatmap.html")
        self.model.save(f"{self.output_folder}/BERTopicmodel")
        
    def write_representative_docs_df(self):
        writer = pd.ExcelWriter(f"{self.output_folder}/representative_docs.xlsx", engine='xlsxwriter')
        for i in self.model.get_representative_docs().keys():
            df = pd.DataFrame(self.model.get_representative_docs()[i], columns=['message'])
            df.to_excel(writer, sheet_name=self.model.get_topic_info()[self.model.get_topic_info()['Topic'] == i]['Name'].values[0][:31])
        writer.close()
        self.model.get_topic_info().to_csv(f"{self.output_folder}/topic_info.csv")

if __name__ == "__main__":
    df_telegram_concat = pd.read_csv("src/machine_learning/BERTopic/df_telegram_test.csv", encoding='UTF-8')
    docs = np.array(df_telegram_concat['text'].tolist(), dtype=object)
    labels = np.array(df_telegram_concat['cluster_id'].tolist(), dtype=int)
    
    output_folder = "src/machine_learning/BERTopic/Result_supervised"
    bertopic_model = OurBERTopicModel(output_folder)
    bertopic_model.fit_model(docs, labels)

    # # Using transform to get new topic assignments
    # new_topics, _ = bertopic_model.model.transform(docs)

    # # Add the new topics as a column to the dataframe
    # df_telegram_concat['new_labelled'] = new_topics

    # # Save the updated dataframe to a new CSV
    # df_telegram_concat.to_csv("src/machine_learning/BERTopic/df_telegram_concat_switzerland_0.65M_labelled.csv", index=False, encoding='UTF-8')
