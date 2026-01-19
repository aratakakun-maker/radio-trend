import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import os

def fetch_data():
    yesterday = datetime.now() - timedelta(days=1)
    url = f"https://www.fmnorth.co.jp/oa/?date={yesterday.strftime('%Y%m%d')}"
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
        songs = []
        for item in soup.select('.oa-list-item'):
            art = item.select_one('.artist')
            ttl = item.select_one('.title')
            if art and ttl:
                songs.append({'artist': art.get_text(strip=True).upper(), 'title': ttl.get_text(strip=True).upper()})
        if songs:
            df = pd.DataFrame(songs)
            ranking = df.groupby(['artist', 'title']).size().reset_index(name='count')
            ranking = ranking.sort_values(by='count', ascending=False).head(50).reset_index(drop=True)
            ranking.insert(0, 'rank', ranking.index + 1)
            ranking['count'] = ranking['count'].astype(str) + "回"
            ranking.to_csv('onair_data.csv', index=False, encoding='utf-8-sig')
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    fetch_data()
