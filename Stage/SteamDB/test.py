import logging

# 設定 log 檔案路徑和 log 級別
log_file = "C:\\Users\\T14 Gen 3\\OneDrive - 輔仁大學\\資料工程師_上課檔案\\專題\\steam_trend\\Data\\GCS_partition\\log\\MostPlayedGames.log"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,  # 設定最低的 log 級別，DEBUG 會記錄所有級別的訊息
    format='%(asctime)s - %(levelname)s - %(message)s',  # 設定 log 訊息的格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 設定日期時間的格式
)

# 測試寫入不同級別的 log 訊息
logging.debug("這是一條 DEBUG 訊息")
logging.info("這是一條 INFO 訊息")
logging.warning("這是一條 WARNING 訊息")
logging.error("這是一條 ERROR 訊息")
logging.critical("這是一條 CRITICAL 訊息")

print(f"Log 檔案已創建並記錄在：{log_file}")
