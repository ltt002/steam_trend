from datetime import datetime
import os
import glob
import pandas as pd
import sys
import logging
import subprocess

# 當天日期
now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d")
#formatted_date = "2024-08-21"    #改之前檔案用
file_date = str(formatted_date)

# 找到資料夾路徑
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
gcs_partition_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))),"Data","GCS_partition")
log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))),"Data","GCS_partition","log")

# GSC路徑
gsutil_partition_path = " gs://tir102-project-database/data/"

def format_MostPlayedGames():
    dir_name = "MostPlayedGames"
    File_ColumnHeading = dir_name + "_ColumnHeading"
    temp_file = (glob.glob(os.path.join(current_dir_path, dir_name, f'*_Temp_{file_date}*.csv')))[0]
    
    #log檔
    log_file = os.path.join(log_path,f'{dir_name}.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,    # 所有都記錄
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # # 讀取執行時間
    # time_str = temp_file.split('_')[-1].split('.')[0].split()[-1]
    # time_formatted = f"{time_str[:2]}:{time_str[2:]}"

    # 處理CSV內容
    df = pd.read_csv(temp_file, header = None, encoding = "utf-8")
    logging.info(f"File: Read from {temp_file}")
    df[0] = df[0].astype(int)
    df[2] = df[2].apply(lambda x: x.split('/')[-3]).astype(str)
    df[3] = df[3].str.replace(',', '').astype(int)
    df[4] = df[4].str.replace(',', '').astype(int)
    df[5] = df[5].str.replace(',', '').astype(int)
    df[6] = formatted_date

    df = df[~df[2].isin(['1422450', '218','2738000','2757350','2877160','3092450','3107080','3132990'])]
    
    # 讀取 File_ColumnHeading 並加到 df 的第一列
    column_heading_file = os.path.join(current_dir_path, dir_name, f'{File_ColumnHeading}.csv')
    column_heading = pd.read_csv(column_heading_file, header=None, encoding="utf-8").iloc[0]

    # 將 column_heading 設定為新的欄名稱
    df.columns = column_heading    
    df = df.head(1000)

    # 按 PeakPlayers 由大到小排序，並加排名
    df = df.sort_values(by='PeakPlayers', ascending=False)
    df['MostPlayedRank'] = range(1, len(df) + 1)
    df = df[['GameID', 'MostPlayedRank', 'PeakPlayers', 'AllTimePeak', 'Date']]

    # 另存新檔
    output_file_path = os.path.join(current_dir_path, dir_name, f'{dir_name}_{file_date}.csv')
    df.to_csv(output_file_path, index=False, encoding='utf-8')

    # 存到 GCS Partition
    gcs_folder_today = os.path.join(gcs_partition_path, dir_name,f'dt={file_date}')
    if os.path.exists(gcs_folder_today):
        logging.warning(f"Folder: Exists {gcs_folder_today}")
    else:
        os.mkdir(os.path.join(gcs_partition_path, dir_name,f'dt={file_date}'))
        logging.info(f"Folder: Created {gcs_folder_today}")
    partition_file_path = os.path.join(gcs_partition_path, dir_name,f'dt={file_date}', f'{dir_name}_{file_date}.csv')
    df.to_csv(partition_file_path, index=False, encoding='utf-8')
    logging.info(f"File: Saved to {partition_file_path}")

    # 使用 subprocess 執行 PowerShell 指令，上傳到GCS
    command_partition = f'gsutil cp -r "{os.path.join(gcs_partition_path, dir_name, "dt="+file_date)}" {gsutil_partition_path}{dir_name}/'
    result = subprocess.run(["powershell", "-Command", command_partition], capture_output=True, text=True)
    logging.info(f'GCS: Uploaded {os.path.join(gcs_partition_path, dir_name, "dt="+file_date)} to {gsutil_partition_path}{dir_name}/ {result.stdout}')

    command_log = f'gsutil cp "{log_file}" {gsutil_partition_path}'
    result = subprocess.run(["powershell", "-Command", command_log], capture_output=True, text=True)
    logging.info(f'GCS: Uploaded {log_file} to {gsutil_partition_path} {result.stdout}')


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
#format_TopRatedGames_All()
#format_TopRatedGames_Y2024()
sys.exit

