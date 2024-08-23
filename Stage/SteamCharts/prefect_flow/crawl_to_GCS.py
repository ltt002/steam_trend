import time
import datetime 
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from google.cloud import storage
import io

# Step1: 爬取資料 取至前5000名，並去除欄位名
top_games_all = []
game_ids = []
r = 1
while r <= 200:
    url = f'https://steamcharts.com/top/p.{r}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        top = soup.find('table',id="top-games", class_='common-table')
        _id = top.find_all('a')
        top_games = top.get_text()
        top_games = re.split(r'[\n\t]', top_games)
        top_games.remove('Name')
        top_games.remove('Current Players')
        top_games.remove('Last 30 Days')
        top_games.remove('Peak Players')
        top_games.remove('Hours Played')
        
        for s in top_games:
            if s != '':
                top_games_all.append(s)

        for link in _id:
            href = link.get('href')
            href = href.split('/app/')[1]
            game_ids.append(href)     
        r += 1
    else:
        break
# Step2: 將取出的資料進行，每5個分組
top_new = []
chunk_size = 5
for i in range(0, len(top_games_all), chunk_size):
    chunk = top_games_all[i:i+chunk_size]
    top_new.append(chunk)
top_new

# Step3: 將資料轉成 DataFrame
columns = ['Rank', 'Name', 'Current_Players', 'Peak_Players', 'Hours_Played(30days)']
data = []
for r in top_new:
    data.append(r)

df = pd.DataFrame(
    data=data,
    columns=columns
)

# Step4: 加入 ID、時間欄位
today = datetime.datetime.now()
date = today.strftime('%Y-%m-%d %H:%M')
_today = today.strftime('%m-%d')
df['Datetime'] = [date for i in range(len(df))]
df.insert(loc=1, column='App_Id', value=game_ids)

# GCS bucket、路徑設置
bucket_name = 'tir102-project-database'  # 替换为你的 GCS bucket 名称
destination_blob_name = f'stage/steamchart/SteamCharts_Rank/SteamCharts_Rank({_today}).csv'

# 將檔案存至內存
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, encoding='utf-8', index=False)

# 創建客戶端 並上傳
service_account_path = 'json_key.json'
storage_client = storage.Client.from_service_account_json(service_account_path)
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')

