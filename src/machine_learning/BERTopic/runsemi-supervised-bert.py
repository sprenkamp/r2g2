import os
import pandas as pd
from bertopic import BERTopic
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

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
    "Volunteering": ["volunteer", "donate", "help", "support", "aid", "assist", "contribute", "доброволец", "пожертвовать", "помощь", "поддержка", "вклад", "Freiwilliger", "spenden", "Hilfe", "Unterstützung", "Beitrag", "assistieren", "beitragen"],
    "Integration": ["community", "integrate", "society", "culture", "local", "mingle", "adapt", "сообщество", "интеграция", "культура", "локальный", "общаться", "адаптировать", "Gemeinschaft", "integrieren", "Gesellschaft", "Kultur", "lokal", "mischen", "anpassen"],
    "Accommodation": ["accommodation", "housing", "shelter", "stay", "rent", "lease", "residence", "accomodation", "жилье", "проживание", "убежище", "аренда", "квартира", "Unterkunft", "Wohnung", "Schutz", "Aufenthalt", "Miete", "Pacht", "Wohnsitz"],
    "Immigration Procedure": ["immigration", "migration", "procedure", "passport", "visa", "status", "citizenship", "иммиграция", "миграция", "процедура", "паспорт", "виза", "гражданство", "Einwanderung", "Migration", "Verfahren", "Pass", "Visum", "Status", "Staatsangehörigkeit"],
    "Social Services": ["service", "benefit", "welfare", "support", "aid", "assistance", "children", "услуга", "поддержка", "благосостояние", "помощь", "дети", "Dienst", "Vorteil", "Sozialhilfe", "Unterstützung", "Hilfe", "Assistenz", "Kinder"],
    "Transport to and from Ukraine": ["transport", "bus", "train", "flight", "route", "border", "Ukraine", "crossing", "транспорт", "автобус", "поезд", "рейс", "маршрут", "граница", "Украина", "Transport", "Bus", "Zug", "Flug", "Strecke", "Grenze", "Ukraine", "Überquerung"],
    "Geopolitical Policy and Sanctions": ["geopolitics", "sanction", "Russia", "tactic", "strategy", "military", "diplomatic", "countermeasure", "economic penalty", "trade restriction", "retaliation", "policy", "war", "геополитика", "санкция", "Россия", "тактика", "стратегия", "военный", "дипломатический", "контрмера", "экономическое наказание", "торговое ограничение", "ответные меры", "война", "Geopolitik", "Sanktion", "Russland", "Taktik", "Strategie", "Militär", "diplomatisch", "Gegenmaßnahme", "wirtschaftliche Strafe", "Handelsbeschränkung", "Vergeltung", "Krieg"],
    "Religious Guidance": ["ecclesiastical", "canonical", "church", "doctrine", "clergy", "sermon", "edict", "declaration", "faith guideline", "pastoral message", "Orthodox", "церковный", "канонический", "церковь", "доктрина", "духовенство", "проповедь", "указ", "декларация", "руководство веры", "пастырское послание", "Православный", "kirchlich", "kanonisch", "Kirche", "Doktrin", "Klerus", "Predigt", "Edikt", "Erklärung", "Glaubensrichtlinie", "pastorale Botschaft", "Orthodox"],
    "Consultate Service": ["consulate", "embassy", "diplomatic", "service", "official", "document", "representative", "консульство", "посольство", "дипломатический", "служба", "официальный", "документ", "Konsulat", "Botschaft", "diplomatisch", "Dienst", "offiziell", "Dokument", "Vertreter"],
    "Banking": ["bank", "finance", "account", "transfer", "currency", "loan", "credit", "банк", "финансы", "счет", "перевод", "валюта", "кредит", "Bank", "Finanzen", "Konto", "Überweisung", "Währung", "Kredit"],
    "Public Transportation and Services": ["public transport", "bus", "metro", "taxi", "ticket", "route", "schedule", "общественный транспорт", "автобус", "метро", "такси", "билет", "маршрут", "расписание", "öffentlicher Verkehr", "Bus", "U-Bahn", "Taxi", "Ticket", "Route", "Fahrplan"],
    "Education": ["school", "education", "university", "study", "student", "teacher", "course", "book", "learn", "школа", "образование", "университет", "учеба", "студент", "учитель", "курс", "книга", "учиться", "Schule", "Bildung", "Universität", "Studium", "Student", "Lehrer", "Kurs", "Buch", "lernen"],
    "Medical": ["hospital", "doctor", "clinic", "medicine", "health", "treatment", "surgery", "больница", "врач", "клиника", "лекарство", "здоровье", "лечение", "хирургия", "Krankenhaus", "Arzt", "Klinik", "Medizin", "Gesundheit", "Behandlung", "Chirurgie"],
    "Legal": ["law", "legal", "court", "judge", "lawyer", "rights", "regulation", "закон", "право", "суд", "судья", "адвокат", "права", "регулирование", "Gesetz", "Recht", "Gericht", "Richter", "Anwalt", "Rechte", "Regelung"],
    "Job and Employment": ["job", "work", "employment", "hire", "salary", "office", "profession", "робота", "работа", "занятость", "наем", "зарплата", "офис", "профессия", "Job", "Arbeit", "Beschäftigung", "einstellen", "Gehalt", "Büro", "Beruf"],
    "Culture and Leisure": ["culture", "art", "museum", "theater", "music", "book", "festival", "культура", "искусство", "музей", "театр", "музыка", "книга", "фестиваль", "Kultur", "Kunst", "Museum", "Theater", "Musik", "Buch", "Festival"],
    "Shopping and Commerce": ["shop", "store", "mall", "buy", "sell", "product", "retail", "магазин", "торговый центр", "покупка", "продажа", "товар", "розница", "Shop", "Geschäft", "Einkaufszentrum", "kaufen", "verkaufen", "Produkt", "Einzelhandel"]
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
        for text in tqdm(self.df['text'], desc="Assigning labels"):
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
        texts = self.df['text'].tolist()

        with tqdm(total=len(texts), desc="Generating embeddings") as pbar:
            def update_pbar(*args, **kwargs):
                pbar.update(len(texts) // 10) 

            embeddings = model.encode(texts, show_progress_bar=update_pbar)
    
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
