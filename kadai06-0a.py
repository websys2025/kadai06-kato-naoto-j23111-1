import requests
import json

APP_ID = "dda9883741613e71b17173269a0b851e1cab39c7"

# APIエンドポイント
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

# 江戸川区の地域コード
cd_area = "13123"  # 東京都 江戸川区

# リクエストパラメータ設定
params = {
    "appId": APP_ID,
    "statsDataId": "0004009600",   # 民間給与実態統計のデータID
    "lang": "J",
    "metaGetFlg": "N",
    "cntGetFlg": "N",
    "sectionHeaderFlg": "1",
    "cdArea": cd_area,
    "replaceSpChars": "0"
}

print(f"\n--- 東京都江戸川区（地域コード: {cd_area}）のデータ ---")

# APIへリクエスト送信
response = requests.get(API_URL, params=params)

# レスポンス確認
if response.status_code == 200:
    data = response.json()
    values = data.get("GET_STATS_DATA", {}).get("STATISTICAL_DATA", {}).get("DATA_INF", {}).get("VALUE", [])

    if not values:
        print("データが見つかりませんでした。")
    else:
        for entry in values[:10]:  # 最初の10件のみ表示
            year = entry.get("@time")
            value = entry.get("$")
            category = entry.get("@cat01")
            print(f"{year}年: {value} （カテゴリ: {category}）")
else:
    print("データ取得に失敗しました。")
