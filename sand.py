import requests
from datetime import datetime
import time
import psycopg2
from supabase import Client, create_client

# 日ごとのapiから取ってきた値をそのままぶち込む
# あと用途を限定させたいから少なくとも現時点では JPY / XXX だけ


# unix時間からdatetimeを算出
today_ut = time.time()

date_today = datetime.fromtimestamp(today_ut)
date_yesterday = datetime.fromtimestamp(today_ut - 86400.00)


def dateToString(date):
    # datetime型から文字列に変換 → 年月日と時間に分割
    str_date = date.strftime("%Y-%m-%d").split(' ')
    return str_date[0]

# print(dateToString(date_today))
# print(dateToString(date_yesterday))


# url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=JPY&to_symbol=USD&apikey=[XXXXXXXX]'
# r = requests.get(url)
# data = r.json()

# print(float(data["Time Series FX (Daily)"][dateToString(date_today)]["4. close"]))

# ["Time Series FX (Daily)"]
# timezone = UTC

# JPY/USDの平均を算出する
# 全関数共通の変数
# currency = 'JPY'

api_key = 'XXXXXX'

# USD AUD CNY CAD THB 

# 一日分のレート
# datetime型を引数にとっても良かったけど
# 何となく他の関数と統一した方が万が一の混乱は避けられるかもしれないと思った
def today_rate(key) :
    payment_code = {
        'USD': [],
        # 'EUR': [],
        # 'GBP': [],
        # 'CHF': [],
        'AUD': [],
        # 'KRW': [],
        'CNY': [],
        # 'IDR': [],
        'CAD': [],
        # 'MYR': [],
        # 'SGD': [],
        # 'HKD': [],
        # 'NZD': [],
        'THB': [],
        # 'NOK': [],
        # 'INR': [],
        # 'PHP': []
        }
    for k in payment_code.keys() :
        url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=JPY&to_symbol={}&apikey={}'.format(k, key)
        rq = requests.get(url)
        tmp = rq.json()
        data = tmp['Time Series FX (Daily)']
        # floatにすると格納されなくてエラーが出る
        # 日付と各日の終値を配列にした後join()で文字列にする
        date_arr = []
        day_rates = []
        for sk in data.keys() :
            date_arr.append(sk)
            day_rates.append(data[sk]['4. close'])
        payment_code[k].append(",".join(date_arr))
        payment_code[k].append(",".join(day_rates))
        time.sleep(5)
    # print(payment_code['USD'][0])
    # print(payment_code['USD'][1])
    return payment_code


# Time Series FX (Daily)

# today_rate(api_key)
jpy_otr_rate = today_rate(api_key)
print(jpy_otr_rate)

# supabaseのライブラリを使った書き込み

# supa_url = "db.mwbijuaheftllmpuwmtt.supabase.co"
# supa_key = "0hXrktyaBb74IURE"
# supabase: Client = create_client(supa_url, supa_key)
# supabase.table("rate").insert({"base_code": "JPY", "payment_code": "XXX", "rate_val": 000, "updated": "XXXX-XX-XX" }).execute()


# supabaseへの書き込み
connection = psycopg2.connect(
    # dbname='unKnown',
    # host='unKnown',
    # user='unKnown',
    # port=0000,
    # password="unKnown",
    dbname='postgres',
    host='db.mwbijuaheftllmpuwmtt.supabase.co',
    user='postgres',
    port=5432,
    password="0hXrktyaBb74IURE"
)

# 直接sql文を送る処理
with connection:
    with connection.cursor() as cursor:
        def sql_write(base="JPY", rate_dic={}):
            [year, month, day] = datetime.fromtimestamp(today_ut).strftime("%Y-%m-%d").split('-')
            updated_val = '-'.join([year, month, day])
            for k, v in rate_dic.items():

                # /updatedにはシングルクォートを忘れないこと
                # v[0], v[1]
                cursor.execute(f"INSERT INTO rate(base_code, payment_code, rate_val, rate_dates, updated) VALUES (\'{base}\', \'{k}\', \'{v[0]}\', \'{v[1]}\', \'{updated_val}\')")
                # cursor.execute(f"UPDATE rate SET rate_val={v}, updated=\'{updated_val}\' WHERE base_code=\'{base}\' AND payment_code=\'{k}\'")
            
        # todayの分
        sql_write(rate_dic=jpy_otr_rate)

    connection.commit()
