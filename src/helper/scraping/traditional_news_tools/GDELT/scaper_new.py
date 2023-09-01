import pandas as pd
import requests
from datetime import datetime

BASE_URL = "http://data.gdeltproject.org/gdeltv2/"
MASTER_FILE_LIST = "masterfilelist.txt"
KEYWORDS = ["Ukraine"]  

def get_latest_files():

    master_list = requests.get(BASE_URL + MASTER_FILE_LIST).text.split('\n')
    return [line.split(' ')[2] for line in master_list if '.export.CSV.zip' in line][-5:]  

def filter_ukraine_refugee_news(file_url):

    df = pd.read_csv(file_url, compression='zip', header=None, delimiter='\t', low_memory=False)

    for _, row in df.iterrows():
        if any(keyword in str(row[57]) for keyword in KEYWORDS):  
            with open('ukraine_refugee_links.txt', 'a') as f:
                f.write(row[58] + '\n')


def main():
    latest_files = get_latest_files()
    for file in latest_files:
        filter_ukraine_refugee_news(file)

if __name__ == "__main__":
    main()
