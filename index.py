import requests
from datetime import datetime
import time
import psycopg2

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

api_key = 'XXXX'

# 一日分のレート
# スケジューラで17個全部回したい(一度に5つのコードまで)要検証
# 優先順位は↓の通り
# USD AUD CNY CAD THB
# EUR GBP CHF KRW IDR
# MYR SGD HKD NZD NOK
# INR PHP
# PHPは値が二つしか取れない(?)

# 終値は多分utcの16:00以降に決まるっぽいから
# 日本時間だと深夜の1時以降頃

def today_rate(key) :
    # データベースに別のテーブルを作って値を管理させる
    # 返ってきた値によってupdateする通貨のグループを分ける
    # テーブル名はstate
    payment_code = {
        'USD': [],
        'AUD': [],
        'CAD': [],
        'TWD': [],
        'CNY': [],

        # 'EUR': [],
        # 'GBP': [],
        # 'CHF': [],
        # 'THB': [],
        # 'SGD': [],

        # 'MYR': [],
        # 'NOK': [],
        # 'INR': [],
        # 'PHP': [],
        # 'KRW': [],
        }
    for k in payment_code.keys() :
        url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=JPY&to_symbol={}&apikey={}'.format(k, key)
        rq = requests.get(url)
        tmp = rq.json()
        # print(tmp)
        data = tmp['Time Series FX (Daily)']
        # 日付と各日の終値を配列にした後join()で文字列にする
        date_arr = []
        day_rates = []
        for sk in data.keys() :
            date_arr.append(sk)
            day_rates.append(data[sk]['4. close'])
        payment_code[k].append(",".join(date_arr))
        payment_code[k].append(",".join(day_rates))
        # time.sleep(5)

    return payment_code


# Time Series FX (Daily)

# today_rate(api_key)
jpy_otr_rate = today_rate(api_key)
# print(jpy_otr_rate)


# supabaseへの書き込み
connection = psycopg2.connect(
    dbname='unKnown',
    host='unKnown',
    user='unKnown',
    port=0000,
    password="unKnown",
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
                # cursor.execute(f"INSERT INTO rate(base_code, payment_code, rate_dates, rate_val, updated) VALUES (\'{base}\', \'{k}\', \'{v[0]}\', \'{v[1]}\', \'{updated_val}\')")
                cursor.execute(f"UPDATE rate SET rate_dates=\'{v[0]}\' ,rate_val=\'{v[1]}\', updated=\'{updated_val}\' WHERE base_code=\'{base}\' AND payment_code=\'{k}\'")
            
        # todayの分
        sql_write(rate_dic=jpy_otr_rate)

    connection.commit()
