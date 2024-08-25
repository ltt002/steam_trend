import time
import datetime 
import pandas as pd
from prefect import flow, task
from google.cloud import storage
import io


@flow(name="normalization")
def normalization():
    today = datetime.datetime.now()
    date = today.strftime('%Y-%m-%d %H:%M')
    _date = today.strftime('%Y-%m-%d')
    _today = today.strftime('%m-%d')
 
    # GCS資料設置
    bucket_name = 'tir102-project-database'
    folder_name = 'stage/steamchart/SteamCharts_Rank'
    file_name = f'SteamCharts_Rank({_today}).csv'
    gcs_file_path = f'{folder_name}/{file_name}'

    # 創建 GCS 客户端
    service_account_path = 'json_key.json'
    storage_client = storage.Client.from_service_account_json(service_account_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_file_path)

    # 下载 GCS 文件到内存
    csv_data = blob.download_as_string()

    # 讀取 CSV 數據並進行處理
    df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), nrows=1000)
    df = df.drop('Rank', axis=1)
    df = df.drop('Name', axis=1)
    df = df.drop('Current_Players', axis=1)
    df = df.drop('Peak_Players', axis=1)

    # 設置輸出檔名、路徑    
    output_file_name = f'test({_today})_normalization.csv'
    output_gcs_path = f'data/SteamCharts_Rank/dt={_date}/{output_file_name}'

    # 將輸出檔案寫入內存
    output_csv_buffer = io.StringIO()
    df.to_csv(output_csv_buffer, encoding='utf-8', index=False)

    # 將檔案上傳至 GCS 指定資料夾
    output_blob = bucket.blob(output_gcs_path)
    output_blob.upload_from_string(output_csv_buffer.getvalue(), content_type='text/csv')



if __name__ == "__main__":
    from prefect_github import GitHubRepository

    normalization.from_source(
        source=GitHubRepository.load("steam-trend"),
        entrypoint="f_normalization_to_GCS.py:normalization",
    ).deploy(
        name="normalization-steamChartsrank-to-gcs",
        tags=["steamcharts_rank", "gcs"],
        work_pool_name="docker",
        job_variables=dict(pull_policy="Never"),
        # parameters=dict(name="Marvin"),
        cron="20 12 * * *"
    )