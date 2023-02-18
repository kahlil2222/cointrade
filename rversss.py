import requests
import pandas as pd
from openpyxl import Workbook
import datetime
import time

# 1년간 데이터를 가져오기 위한 날짜 설정
end = int(datetime.datetime.now().timestamp() * 1000)
start = end - (365 * 24 * 60 * 60 * 1000)

# API 호출을 통한 데이터 가져오기
url = "https://api.upbit.com/v1/candles/minutes/5"
querystring = {"market":"KRW-BTC","count":"1000"}
headers = {"Accept": "application/json"}
data = []

while True:
    querystring["to"] = str(end)
    querystring["from"] = str(end - (1000 * 5 * 60 * 1000))
    response = requests.request("GET", url, headers=headers, params=querystring)
    try:
        response_data = response.json()
    except:
        break
    if not response_data:
        break
    data += response_data
    end -= 1000 * 5 * 60 * 1000
    if end < start:
        break
    time.sleep(5)  # 1초간 대기

# 데이터를 데이터프레임으로 변환하고 엑셀 파일에 저장하기
df = pd.DataFrame(data, columns=["candle_date_time_kst", "opening_price", "high_price", "low_price", "trade_price", "candle_acc_trade_volume"])
df["candle_date_time_kst"] = pd.to_datetime(df["candle_date_time_kst"])
df.set_index("candle_date_time_kst", inplace=True)
df.sort_index(ascending=True, inplace=True)

wb = Workbook()
ws = wb.active

for i, row in df.iterrows():
    ws.append([i, row["opening_price"], row["high_price"], row["low_price"], row["trade_price"], row["candle_acc_trade_volume"]])

wb.save("btc_data.xlsx")
print("Data saved to btc_data.xlsx")