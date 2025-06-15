import requests
import pandas as pd

# World Bank APIエンドポイント（中国のGDP）
API_URL = "https://api.worldbank.org/v2/country/CHN/indicator/NY.GDP.MKTP.CD"

params = {
    "format": "json",  # JSON形式で取得
    "per_page": 10     # 最新の10年分を取得
}

# APIからデータ取得
response = requests.get(API_URL, params=params)
data = response.json()

# データが正しく取得できたか確認
if response.status_code == 200 and len(data) > 1:
    stats_data = data[1]

    # DataFrameに変換
    df = pd.DataFrame(stats_data)

    # 国名・指標名を抽出
    df['国名'] = df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else x)
    df['指標名'] = df['indicator'].apply(lambda x: x['value'] if isinstance(x, dict) else x)

    # 列名を日本語に
    col_rename = {
        'date': '年',
        'value': 'GDP（USD）',
        '国名': '国名',
        '指標名': '指標名'
    }

    df_simple = df[['date', 'value', '国名', '指標名']].rename(columns=col_rename)

    # 年順にソート（降順）
    df_simple = df_simple.sort_values('年', ascending=False).reset_index(drop=True)

    # GDPを見やすい表示（兆ドル単位で桁区切り付き）
    df_simple['GDP（兆USD）'] = df_simple['GDP（USD）'].apply(
        lambda x: f"{x/1e12:.2f} 兆USD" if pd.notnull(x) else "N/A"
    )

    # 結果を表示
    print("\n✅ 中国の名目GDP（最新10年）:")
    print(df_simple[['年', '国名', 'GDP（兆USD）', '指標名']])

else:
    print("❌ データの取得に失敗しました。")
