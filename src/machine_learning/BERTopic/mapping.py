# topic_to_category_mapping = {
#     "Volunteering and Donations": "Volunteering",
#     "Local Communities": "Integration", 
#     "Accomodation": "Accomodation",
#     "Migration Apart from Ukraine": "Immigration Procedure", 
#     "Problems Refugee Management": "Social Services",  
#     "Current Information Refugees": "Integration",  
#     "Sanktions Russia and War Strategy": None, 
#     "Current Information War": None,  
#     "Refugee Routes from Ukraine": "Transport to and from Urkraine",
#     "Children and Human Rights": "Social Services", 
#     "Statements by the Church": None 
# }

cluster_keywords_mapping = {
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

    "Geopolitical Policy and Sanctions": {
        "keywords": ["geopolitics", "sanction", "Russia", "tactic", "strategy", "military", "diplomatic", "countermeasure", "economic penalty", "trade restriction", "retaliation", "policy", "war",
                     "геополитика", "санкция", "Россия", "тактика", "стратегия", "военный", "дипломатический", "контрмера", "экономическое наказание", "торговое ограничение", "ответные меры", "война",
                     "Geopolitik", "Sanktion", "Russland", "Taktik", "Strategie", "Militär", "diplomatisch", "Gegenmaßnahme", "wirtschaftliche Strafe", "Handelsbeschränkung", "Vergeltung", "Krieg"]
    },
    
    "Religious Guidance": {
        "keywords": ["ecclesiastical", "canonical", "church", "doctrine", "clergy", "sermon", "edict", "declaration", "faith guideline", "pastoral message", "Orthodox",
                     "церковный", "канонический", "церковь", "доктрина", "духовенство", "проповедь", "указ", "декларация", "руководство веры", "пастырское послание", "Православный",
                     "kirchlich", "kanonisch", "Kirche", "Doktrin", "Klerus", "Predigt", "Edikt", "Erklärung", "Glaubensrichtlinie", "pastorale Botschaft", "Orthodox"]
    },

    "Consultate Service": {
        "keywords": ["consulate", "embassy", "diplomatic", "service", "official", "document", "representative",
                     "консульство", "посольство", "дипломатический", "служба", "официальный", "документ",
                     "Konsulat", "Botschaft", "diplomatisch", "Dienst", "offiziell", "Dokument", "Vertreter"]
    },

    "Banking": {
        "keywords": ["bank", "finance", "account", "transfer", "currency", "loan", "credit",
                     "банк", "финансы", "счет", "перевод", "валюта", "кредит",
                     "Bank", "Finanzen", "Konto", "Überweisung", "Währung", "Kredit"]
    },

    "Public Transportation and Services": {
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

    "Carriers": {
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

#connect to db
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://refugeeukraineai_test:FKFSPyoomgVAkufs@cluster0.fcobsyq.mongodb.net/")
db = cluster["test"]
collection = db["cluster"]

for document in collection.find():
    cluster_content = document.get('cluster', '').lower()
    matched_cluster = "unknown cluster"  

    for cluster_name, cluster_info in cluster_keywords_mapping.items():
        if any(keyword.lower() in cluster_content for keyword in cluster_info['keywords']):
            matched_cluster = cluster_name
            break 

    collection.update_one(
        {"_id": document["_id"]}, 
        {"$set": {"cluster_fixed": matched_cluster}}
    )








