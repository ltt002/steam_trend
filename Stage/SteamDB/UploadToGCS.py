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
#formatted_date = "2024-08-14"    #改之前檔案用
file_date = str(formatted_date)

# 找到資料夾路徑
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
gcs_partition_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))),"Data","GCS_partition")
log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_file_path))),"Data","GCS_partition","log")

# GSC路徑
gsutil_partition_path = "gs://steam_trend/partition/"

def upload_gcs():
    dir_name = "MostPlayedGames"
    File_ColumnHeading = dir_name + "_ColumnHeading"
    
    #log檔
    log_file = os.path.join(log_path,f'{dir_name}.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,    # 所有都記錄
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 使用 subprocess 執行 PowerShell 指令，上傳到GCS
    # command_partition = 'gsutil cp -r "C:/Users/T14 Gen 3/OneDrive - 輔仁大學/資料工程師_上課檔案/專題/steam_trend/Data/GCS_partition/MostPlayedGames/" gs://steam_trend/partition/'
    # result = subprocess.run(["powershell", "-Command", command_partition], capture_output=True, text=True)
    # logging.info(f'GCS: Uploaded {gsutil_partition_path}{dir_name}/ {result.stdout}')

    # command_log = 'gsutil cp "C:/Users/T14 Gen 3/OneDrive - 輔仁大學/資料工程師_上課檔案/專題/steam_trend/Data/GCS_partition/log/MostPlayedGames.log" gs://steam_trend/partition/log/'
    # result = subprocess.run(["powershell", "-Command", command_log], capture_output=True, text=True)
    # logging.info(f'GCS: Uploaded {gsutil_partition_path}/log/ {result.stdout}')
    print(f'gsutil cp -r {os.path.join(gcs_partition_path, dir_name, "dt="+file_date)} {gsutil_partition_path}{dir_name}/')

# gsutil cp -r "C:/Users/T14 Gen 3/OneDrive - 輔仁大學/資料工程師_上課檔案/專題/steam_trend/Data/GCS_partition/MostPlayedGames/" gs://steam_trend/partition/
# gsutil cp "C:/Users/T14 Gen 3/OneDrive - 輔仁大學/資料工程師_上課檔案/專題/steam_trend/Data/GCS_partition/log/MostPlayedGames.log" gs://steam_trend/partition/log/




# 執行
upload_gcs()
sys.exit

