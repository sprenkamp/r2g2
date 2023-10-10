# This code deals with organizing and processing data for future use of semi-supervised bertopic
# Number of data entries with cluster_id as -1: 2229067 
# Number of data entries with cluster_id not equal to -1: 369609. 
# (labelled topic : unlabelled topic = 4：25）
# import file: df_telegram_test.csv, export file: df_telegram_concat.csv, the name of output could be different due to the sample needed.
# In our case, we only extract 100,000 labelled data.

import pandas as pd
from pymongo import MongoClient
import pandas as pd
from tqdm import tqdm
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import re

# Create a Cluster Mapping by translating the dictionary into numeric representation:
#{'Volunteering': 0, 'Integration': 1, 'Accommodation': 2, 
# 'Immigration Procedure': 3, 'Social Services': 4, 'Transport to and from Ukraine': 5, 
# 'Consultate Services': 6, 'Banking': 7, 'Public Transport and Services': 8, 
# 'Education': 9, 'Job and Development Opportunities': 10, 'Interpretation and Translation Services': 11, 
# 'Carriers, Transport to and from Ukraine': 12, 'Medical Information': 13, 'Asylum': 14, 
# 'Transport Personal Car': 15, 'Dentistry Information': 16, 'Network Provider': 17, 
# 'Veterinarian and Vaccination': 18}

topic_keywords = cluster_keywords_mapping = {
    "Volunteering": {
        "keywords": ["volunteer", "donate", "help", "support", "aid", "assist", "contribute",
                     "доброволец", "пожертвовать", "помощь", "поддержка", "вклад",
                     "Freiwilliger", "spenden", "Hilfe", "Unterstützung", "Beitrag", "assistieren", "beitragen"]
    },

    "Integration": {
        "keywords": ["community", "integrate", "society", "culture", "local", "mingle", "adapt",
                     "сообщество", "интеграция", "культура", "локальный", "общаться", "адаптировать",
                     "Gemeinschaft", "integrieren", "Gesellschaft", "Kultur", "lokal", "mischen", "anpassen"]
    },

    "Accommodation": {
        "keywords": ["accommodation", "housing", "shelter", "stay", "rent", "lease", "residence", "accomodation",
                     "жилье", "проживание", "убежище", "аренда", "квартира",
                     "Unterkunft", "Wohnung", "Schutz", "Aufenthalt", "Miete", "Pacht", "Wohnsitz"]
    },

    "Immigration Procedure": {
        "keywords": ["immigration", "migration", "procedure", "passport", "visa", "status", "citizenship",
                     "иммиграция", "миграция", "процедура", "паспорт", "виза", "гражданство",
                     "Einwanderung", "Migration", "Verfahren", "Pass", "Visum", "Status", "Staatsangehörigkeit"]
    },

    "Social Services": {
        "keywords": ["service", "benefit", "welfare", "support", "aid", "assistance", "children",
                     "услуга", "поддержка", "благосостояние", "помощь", "дети",
                     "Dienst", "Vorteil", "Sozialhilfe", "Unterstützung", "Hilfe", "Assistenz", "Kinder"]
    },

    "Transport to and from Ukraine": {
        "keywords": ["transport", "bus", "train", "flight", "route", "border", "Ukraine", "crossing",
                     "транспорт", "автобус", "поезд", "рейс", "маршрут", "граница", "Украина",
                     "Transport", "Bus", "Zug", "Flug", "Strecke", "Grenze", "Ukraine", "Überquerung"]
    },

    "Consultate Services": {
        "keywords": ["consulate", "embassy", "diplomatic", "service", "official", "document", "representative",
                     "консульство", "посольство", "дипломатический", "служба", "официальный", "документ",
                     "Konsulat", "Botschaft", "diplomatisch", "Dienst", "offiziell", "Dokument", "Vertreter"]
    },

    "Banking": {
        "keywords": ["bank", "finance", "account", "transfer", "currency", "loan", "credit",
                     "банк", "финансы", "счет", "перевод", "валюта", "кредит",
                     "Bank", "Finanzen", "Konto", "Überweisung", "Währung", "Kredit"]
    },

    "Public Transport and Services": {
        "keywords": ["public transport", "bus", "metro", "taxi", "ticket", "route", "schedule",
                     "общественный транспорт", "автобус", "метро", "такси", "билет", "маршрут", "расписание",
                     "öffentlicher Verkehr", "Bus", "U-Bahn", "Taxi", "Ticket", "Route", "Fahrplan"]
    },
    
    "Education": {
        "keywords": ["school", "education", "university", "study", "student", "teacher", "course", "book", "learn",
                     "школа", "образование", "университет", "учеба", "студент", "учитель", "курс", "книга", "учиться",
                     "Schule", "Bildung", "Universität", "Studium", "Student", "Lehrer", "Kurs", "Buch", "lernen"]
    },
    
    "Job and Development Opportunities": {
        "keywords": ["job", "employment", "opportunity", "career", "vacancy", "interview", "hire",
                     "работа", "занятость", "возможность", "карьера", "вакансия", "собеседование", "найм",
                     "Job", "Beschäftigung", "Möglichkeit", "Karriere", "Vakanz", "Interview", "Einstellung"]
    },

    "Interpretation and Translation Services": {
        "keywords": ["interpretation", "translation", "language", "service", "document", "speak", "translate",
                     "толкование", "перевод", "язык", "служба", "документ", "говорить", "перевести",
                     "Interpretation", "Übersetzung", "Sprache", "Dienst", "Dokument", "sprechen", "übersetzen"]
    },

    "Carriers, Transport to and from Ukraine": {
        "keywords": ["carrier", "transport", "logistics", "shipment", "cargo", "delivery", "package",
                     "перевозчик", "транспорт", "логистика", "поставка", "груз", "доставка", "пакет",
                     "Transporteur", "Transport", "Logistik", "Sendung", "Fracht", "Lieferung", "Paket"]
    },

    "Medical Information": {
        "keywords": ["medical", "health", "hospital", "clinic", "doctor", "medicine", "treatment",
                     "медицинский", "здоровье", "больница", "клиника", "врач", "лекарство", "лечение",
                     "medizinisch", "Gesundheit", "Krankenhaus", "Klinik", "Arzt", "Medizin", "Behandlung"]
    },

    "Asylum": {
        "keywords": ["asylum", "protection", "application", "status", "safe", "permit",
                     "убежище", "защита", "заявка", "статус", "безопасный", "разрешение",
                     "Asyl", "Schutz", "Antrag", "Status", "sicher", "Erlaubnis"]
    },

    "Transport Personal Car": {
        "keywords": ["car", "vehicle", "drive", "license", "personal transport",
                     "машина", "транспортное средство", "водить", "лицензия", "личный транспорт",
                     "Auto", "Fahrzeug", "fahren", "Lizenz", "persönlicher Transport"]
    },

    "Dentistry Information": {
        "keywords": ["dentistry", "dentist", "tooth", "clinic", "oral", "treatment", "dental care",
                     "стоматология", "стоматолог", "зуб", "клиника", "оральный", "лечение", "зубной уход",
                     "Zahnmedizin", "Zahnarzt", "Zahn", "Klinik", "oral", "Behandlung", "Zahnpflege"]
    },

    "Network Provider": {
        "keywords": ["network", "provider", "internet", "mobile", "connectivity", "service", "data",
                     "сеть", "поставщик", "интернет", "мобильный", "соединение", "служба", "данные",
                     "Netzwerk", "Anbieter", "Internet", "mobil", "Konnektivität", "Dienst", "Daten"]
    },

    "Veterinarian and Vaccination": {
        "keywords": ["veterinarian", "vet", "animal", "pet", "treatment", "clinic", "vaccination",
                     "ветеринар", "животное", "питомец", "лечение", "клиника", "вакцинация",
                     "Tierarzt", "Tier", "Haustier", "Behandlung", "Klinik", "Impfung"]
    }
}

cluster_mapping = {topic: idx for idx, topic in enumerate(topic_keywords.keys())}

print(cluster_mapping)

# Load an existing CSV, map the cluster names to the corresponding cluster IDs
# Change it into your own local path if need to run, several typos of cluster_name is modified(e.g., accomodation, consulate, Public Transport and Service, Transport personal Car..)in original doc, please refer to the above key of dictionary
file_path = "src/machine_learning/BERTopic/df_telegram_test.csv" 
df = pd.read_csv(file_path, encoding='UTF-8')
df['cluster_id'] = df['cluster_name'].map(cluster_mapping)
# df.to_csv(file_path, index=False)

# Fetch Data from MongoDB
client = MongoClient("mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(ATLAS_USER, ATLAS_TOKEN))
db = client.get_database("scrape")
collection = db["telegram"]

# swiss_data_cursor = collection.find({"country": "Switzerland"}, {"messageText": 1, "_id": 0}).limit(500000)
# swiss_data_list = list(tqdm(swiss_data_cursor, total=min(500000, collection.count_documents({"country": "Switzerland"}))))

# Fetch only 'messageText' from data where the country is Switzerland
swiss_data_cursor = collection.find({"country": "Switzerland"}, {"messageText": 1, "_id": 0})
swiss_data_list = list(tqdm(swiss_data_cursor, total=collection.count_documents({"country": "Switzerland"})))

# Convert the fetched data to DataFrame
df_swiss = pd.DataFrame(swiss_data_list)
df_swiss.columns = ['text']
df_swiss['cluster_name'] = None
df_swiss['cluster_id'] = -1

#Extract 100000 data in sequence from labelled dataset
df_subset = df.head(100000)

# Concatenate the Switzerland data with the existing DataFrame and save it to a new CSV file
df_combined = pd.concat([df_subset, df_swiss], ignore_index=True)

def remove_links(text):
    return re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

def remove_emojis(text):
    # The pattern will recognize most of the emojis in the text
    emoji_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  
        "]+", flags = re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Apply preprocessing
df_combined['text'] = df_combined['text'].apply(remove_links).apply(remove_emojis)

# Drop rows where 'text' column is either NaN or empty string
df_combined.dropna(subset=['text'], inplace=True)
df_combined = df_combined[df_combined['text'].str.strip() != ""]

# Save the processed dataset, to note, 0.65M includeds all the swiss data.
df_combined.to_csv("src/machine_learning/BERTopic/df_telegram_concat_switzerland_0.65M_v2.csv", index=False, encoding='UTF-8')
