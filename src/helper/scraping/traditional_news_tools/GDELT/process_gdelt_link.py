import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import concurrent.futures

def fetch_content(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(link, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = "\n".join(p.text for p in paragraphs)
        return content.strip() 
    except Exception as e:
        print(f"Error fetching content for link {link}: {e}")
        return ""

filepath = os.path.join("r2g2", "src", "helper", "scraping", "traditional_news_tools", "GDELT", "bquxjob_1844ec48_18a2b4ef93a.json")
df = pd.read_json(filepath)

# 清理数据
df = df.dropna(subset=['Link'])  
df = df[df['Link'].str.len() < 5000] 

contents = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for content in tqdm(executor.map(fetch_content, df['Link']), total=len(df)):
        contents.append(content)

df['Link_Content'] = contents

df = df[df['Link_Content'] != "The page may have moved, you may have mistyped the address, or followed a bad link"]

output_path_json = os.path.join(os.getcwd(), "updated_bq_results.json")
df.to_json(output_path_json, orient='records', lines=True)

output_path_csv = os.path.join(os.getcwd(), "updated_bq_results.csv")
df.to_csv(output_path_csv, index=False)
