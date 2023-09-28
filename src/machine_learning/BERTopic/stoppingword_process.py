import nltk
import re
import pandas as pd
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from bertopic import BERTopic

# Download required NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize an empty list to hold the stopwords
stopWords = []

# Define and extend the stopwords list
languages = ['english', 'german', 'french', 'italian', 'russian']
for lang in languages:
    stopWords.extend(stopwords.words(lang))  # Use extend to add multiple items to the list

# Adding Ukrainian stopwords
with open("data/stopwords/stopwords_ua.txt", encoding='utf-8') as file:
    ukrstopWords = [line.rstrip() for line in file]  # Reading lines from file and storing them in a list
    stopWords.extend(ukrstopWords) 

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

# Load your dataset
df_telegram_concat = pd.read_csv("src/machine_learning/BERTopic/df_telegram_concat_switzerland.csv", encoding='UTF-8')

# Apply preprocessing
df_telegram_concat['text'] = df_telegram_concat['text'].apply(remove_links).apply(remove_emojis)

# Drop rows where 'text' column is either NaN or empty string
df_telegram_concat.dropna(subset=['text'], inplace=True)
df_telegram_concat = df_telegram_concat[df_telegram_concat['text'].str.strip() != ""]

# Save the processed dataset
df_telegram_concat.to_csv("src/machine_learning/BERTopic/df_telegram_concat_switzerland.csv", index=False, encoding='UTF-8')
