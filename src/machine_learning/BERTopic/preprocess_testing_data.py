# This code deals with organizing and processing data for future use of semi-supervised bertopic
# Number of data entries with cluster_id as -1: 2229067 
# Number of data entries with cluster_id not equal to -1: 369609. 
# (labelled topic : unlabelled topic = 4：25）
# import file: df_telegram_test.csv, export file: df_telegram_concat.csv
import pandas as pd
from pymongo import MongoClient
import pandas as pd
from tqdm import tqdm

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
# Change it into your own local path if need to run, several typos of cluster_name is modified(e.g., accomodation, consulate..)in original doc, please refer to the new df_telegram.csv
file_path = r"C:\Users\rocco\Documents\project0809\r2g2\src\machine_learning\BERTopic\df_telegram.csv" 
df = pd.read_csv(file_path, encoding='ISO-8859-1')
df['cluster_id'] = df['cluster_name'].map(cluster_mapping)
df.to_csv(file_path, index=False)

# Fetch Data from MongoDB
client = MongoClient("mongodb+srv://refugeeukraineai_test:FKFSPyoomgVAkufs@cluster0.fcobsyq.mongodb.net/")
db = client.get_database("scrape")
collection = db["telegram"]

data = list(tqdm(collection.find(), total=collection.count_documents({})))

df_mongo = pd.DataFrame(data)

df_mongo = df_mongo[['messageText']]
df_mongo.columns = ['text']

df_mongo['cluster_name'] = None
df_mongo['cluster_id'] = -1

file_path = r"C:\Users\rocco\Documents\project0809\r2g2\src\machine_learning\BERTopic\df_telegram_test.csv"
df_telegram = pd.read_csv(file_path, encoding='ISO-8859-1')

# loads another CSV file and concatenates it with the previously processed MongoDB data with columns of cluster_name, cluster_id, text.
df_combined = pd.concat([df_telegram, df_mongo], ignore_index=True)

df_combined.to_csv(r"C:\Users\rocco\Documents\project0809\r2g2\src\machine_learning\BERTopic\df_telegram_concat.csv", index=False)
