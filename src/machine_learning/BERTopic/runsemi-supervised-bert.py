import os
import pandas as pd
from bertopic import BERTopic
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer

nltk.download('stopwords')

# Define stopwords
stopWords = stopwords.words('english')
languages = ['german', 'french', 'italian', 'russian']
for lang in languages:
    for word in stopwords.words(lang):
        stopWords.append(word)

with open("data/stopwords/stopwords_ua.txt") as file:
    ukrstopWords = [line.rstrip() for line in file]
for stopwords in ukrstopWords:
    stopWords.append(stopwords)

seed_topic_list = {
    "Volunteering": ["volunteer", "donate", "help"],
    "Integration": ["community", "integrate", "society"],
    "Accommodation": ["accommodation", "housing", "shelter"],
    "Immigration Procedure": ["immigration", "migration", "procedure"],
    "Social Services": ["service", "benefit", "welfare"],
    "Transport to and from Ukraine": ["transport", "bus", "train"],
    "Geopolitical Policy and Sanctions": ["geopolitics", "sanction", "Russia"],
    "Religious Guidance": ["ecclesiastical", "canonical", "church"],
    "Consultate Service": ["consulate", "embassy", "diplomatic"],
    "Banking": ["bank", "finance", "account"],
    "Public Transportation and Services": ["public transport", "bus", "metro"],
    "Education": ["school", "education", "university"],
    "Job and Development Opportunities": ["job", "employment", "opportunity"],
    "Interpretation and Translation Services": ["interpretation", "translation", "language"],
    "Carriers": ["carrier", "transport", "logistics"],
    "Medical Information": ["medical", "health", "hospital"],
    "Asylum": ["asylum", "protection", "application"],
    "Transport Personal Car": ["car", "vehicle", "drive"],
    "Dentistry Information": ["dentistry", "dentist", "tooth"],
    "Network Provider": ["network", "provider", "internet"],
    "Veterinarian and Vaccination": ["veterinarian", "vet", "animal"]
}

class BERTopicAnalysis:
    def __init__(self, input_data, output_folder):
        self.input_data = input_data
        self.output_folder = output_folder

    def load_data(self):
        self.df = pd.read_csv(self.input_data)
        self.df.dropna(subset=['text'], inplace=True)
        self.df.drop_duplicates(subset=['text'], keep='first', inplace=True)
        self.df["text"] = self.df['text'].str.split().str.join(' ')

    def get_labels_from_seed(self):
        labels = []
        for text in self.df['text']:
            assigned = False
            for topic, keywords in seed_topic_list.items():
                if any(keyword in text for keyword in keywords):
                    labels.append(topic)
                    assigned = True
                    break
            if not assigned:
                labels.append(-1)
        return labels

    def get_document_embeddings(self):
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  
        embeddings = model.encode(self.df['text'].tolist())
        return embeddings

    def fit_BERTopic(self):
        y = self.get_labels_from_seed()
        vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words=stopWords)
        self.model = BERTopic(verbose=True, language="multilingual", vectorizer_model=vectorizer_model)
        
        embeddings = self.get_document_embeddings()
        topics, probs = self.model.fit_transform(embeddings, y)

    def save_results(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        self.df["topic"] = topics
        self.df.to_csv(f"{self.output_folder}/df_model.csv", index=False)

    def run_all(self):
        self.load_data()
        self.fit_BERTopic()
        self.save_results()

def main():
    input_data = "src/machine_learning/BERTopic/df_telegram.csv"
    output_folder = "src/machine_learning/BERTopic"

    bertopic_analysis = BERTopicAnalysis(input_data, output_folder)
    bertopic_analysis.run_all()

if __name__ == "__main__":
    main()
