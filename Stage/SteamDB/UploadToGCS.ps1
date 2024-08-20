# 設定來源路徑和目標路徑
$sourcePath = "C:/Users/T14 Gen 3/OneDrive - 輔仁大學/資料工程師_上課檔案/專題/steam_trend/Data/GCS_partition/MostPlayedGames/"
$destinationPath = "gs://steam_trend/partition/"

# 使用 gsutil 工具進行檔案複製
gsutil cp -r $sourcePath $destinationPath
