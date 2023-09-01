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
        return content
    except Exception as e:
        print(f"Error fetching content for link {link}: {e}")
        return ""

filepath = os.path.join("r2g2", "src", "helper", "scraping", "traditional_news_tools", "GDELT", "bquxjob_1844ec48_18a2b4ef93a.json")
df = pd.read_json(filepath)

df_sample = df.head(100).copy()

contents = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for content in tqdm(executor.map(fetch_content, df_sample['Link']), total=len(df_sample)):
        contents.append(content)

df_sample['Link_Content'] = contents

output_path_json = os.path.join(os.getcwd(), "trail_updated_bq_results.json")
df_sample.to_json(output_path_json, orient='records', lines=True)

output_path_csv = os.path.join(os.getcwd(), "trail_updated_bq_results.csv")
df_sample.to_csv(output_path_csv, index=False)
