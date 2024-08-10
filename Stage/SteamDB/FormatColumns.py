from datetime import datetime
import os
import glob
import pandas as pd
import sys

# 當天日期
now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d")
#formatted_date = "2024-08-06"    #改之前檔案用
file_date = str(formatted_date)

# 找到資料夾路徑
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)

def format_MostPlayedGames():
    dir_name = "MostPlayedGames"
    File_ColumnHeading = dir_name + "_ColumnHeading"
    temp_file = (glob.glob(os.path.join(current_dir_path, dir_name, f'*_Temp_{file_date}*.csv')))[0]
    
    # # 讀取執行時間
    # time_str = temp_file.split('_')[-1].split('.')[0].split()[-1]
    # time_formatted = f"{time_str[:2]}:{time_str[2:]}"

    # 處理CSV內容
    df = pd.read_csv(temp_file, header = None, encoding = "utf-8")
    df[0] = df[0].astype(int)
    df[2] = df[2].apply(lambda x: x.split('/')[-3]).astype(str)
    df[3] = df[3].str.replace(',', '').astype(int)
    df[4] = df[4].str.replace(',', '').astype(int)
    df[5] = df[5].str.replace(',', '').astype(int)
    df[6] = formatted_date
    
    # 讀取 File_ColumnHeading 並加到 df 的第一列
    column_heading_file = os.path.join(current_dir_path, dir_name, f'{File_ColumnHeading}.csv')
    column_heading = pd.read_csv(column_heading_file, header=None, encoding="utf-8").iloc[0]

    # 將 column_heading 設定為新的欄名稱
    df.columns = column_heading

    # 依Table欄位儲存
    df = df[['GameID', 'Rank', 'PeakPlayers', 'AllTimePeak', 'Date']]

    # 另存新檔
    output_file_path = os.path.join(current_dir_path, dir_name, f'{dir_name}_{file_date}.csv')
    df.to_csv(output_file_path, index=False, encoding='utf-8')


def format_TopRatedGames_All():
    dir_name = "TopRatedGames"
    file_name_mid = "AllTime"
    File_ColumnHeading = f"{dir_name}_{file_name_mid}_ColumnHeading"
    temp_file = (glob.glob(os.path.join(current_dir_path, dir_name, f'*{file_name_mid}_Temp_{file_date}*.csv')))[0]
    
    # # 讀取執行時間
    # time_str = temp_file.split('_')[-1].split('.')[0].split()[-1]
    # time_formatted = f"{time_str[:2]}:{time_str[2:]}"

    # 處理CSV內容
    df = pd.read_csv(temp_file, header = None, encoding = "utf-8")
    df[0] = df[0].astype(int)
    df[2] = df[2].apply(lambda x: x.split('/')[-2]).astype(str)
    df[3] = df[3].str.replace(',', '').astype(int)
    df[4] = df[4].str.replace(',', '').astype(int)
    df[5] = df[5].str.replace(',', '').astype(int)
    df[6] = df[6].str.replace('%', '').astype(float)/100
    df[7] = formatted_date
        
    # 讀取 File_ColumnHeading 並加到 df 的第一列
    column_heading_file = os.path.join(current_dir_path, dir_name, f'{File_ColumnHeading}.csv')
    column_heading = pd.read_csv(column_heading_file, header=None, encoding="utf-8").iloc[0]

    # 將 column_heading 設定為新的欄名稱
    df.columns = column_heading

    # 依Table欄位儲存
    df = df[['GameID', 'Rank', "Positive", "Negative", "Total", "Rating", "Date"]]
 
    # 另存新檔
    output_file_path = os.path.join(current_dir_path, dir_name, f'{dir_name}_{file_name_mid}_{file_date}.csv')
    df.to_csv(output_file_path, index=False, encoding='utf-8')


def format_TopRatedGames_Y2024():
    dir_name = "TopRatedGames"
    file_name_mid = "Y2024"
    temp_file = (glob.glob(os.path.join(current_dir_path, dir_name, f'*{file_name_mid}_Temp_{file_date}*.csv')))[0]
    
    # 讀取執行時間
    time_str = temp_file.split('_')[-1].split('.')[0].split()[-1]
    time_formatted = f"{time_str[:2]}:{time_str[2:]}"

    # 處理CSV內容
    df = pd.read_csv(temp_file, header = None, encoding = "utf-8")
    df[0] = df[0].astype(int)
    df[2] = df[2].apply(lambda x: x.split('/')[-2]).astype(str)
    df[3] = df[3].str.replace('%', '').astype(float)/100
    df[4] = df[4].str.replace(',', '').replace('—', '0').astype(int)
    df[5] = df[5].str.replace(',', '').replace('—', '0').astype(int)
    df[6] = formatted_date + " " + time_formatted

    # 另存新檔
    output_file_path = os.path.join(current_dir_path, dir_name, f'{dir_name}_{file_name_mid}_{file_date}.csv')
    df.to_csv(output_file_path, index=False, header=False, encoding='utf-8')

# 執行
format_MostPlayedGames()
format_TopRatedGames_All()
#format_TopRatedGames_Y2024()
sys.exit

