import requests
from datetime import datetime
import time
import psycopg2

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

# 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=JPY&to_symbol=[XXX]&apikey=[XXXXXXXXXXX]' * 17
# 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=[XXX]&to_symbol=JPY&apikey=[XXXXXXXXXXX]' * 17
# ["Time Series FX (Daily)"]
# timezone = UTC

# JPY/USDの平均を算出する
# 全関数共通の変数
# currency = 'JPY'

api_key = 'XXXXXX'

# 一日分のレート
# datetime型を引数にとっても良かったけど
# 何となく他の関数と統一した方が万が一の混乱は避けられるかもしれないと思った
def one_day_rate(date, key) :
    payment_code = {
        'USD': 0,
        'EUR': 0,
        'GBP': 0,
        'CHF': 0,
        'AUD': 0,
        'KRW': 0,
        'CNY': 0,
        'IDR': 0,
        'CAD': 0,
        'MYR': 0,
        'SGD': 0,
        'HKD': 0,
        'NZD': 0,
        'THB': 0,
        'NOK': 0,
        'INR': 0,
        'PHP': 0
        }
    for k in payment_code.keys() :
        url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=JPY&to_symbol={}&apikey={}'.format(k, key)
        rq = requests.get(url)
        data = rq.json()
        # floatにすると格納されなくてエラーが出る
        # payment_code[k] = float(data['Time Series FX (Daily)'][date]['4. close'])
        payment_code[k] = data['Time Series FX (Daily)'][date]['4. close']
        # print(k)
        time.sleep(10)
    return payment_code

# Time Series FX (Daily)

today_jpy_XXX_rate = one_day_rate(dateToString(date_today), api_key)

# 〇〇〇 / JPYのレートを取得(今日の分のみ)
# def today_rate_jpy(date, key) :
#     base_code = {
#         'USD': 0,
#         'EUR': 0,
#         'GBP': 0,
#         'CHF': 0,
#         'AUD': 0,
#         'KRW': 0,
#         'CNY': 0,
#         'IDR': 0,
#         'CAD': 0,
#         'MYR': 0,
#         'SGD': 0,
#         'HKD': 0,
#         'NZD': 0,
#         'THB': 0,
#         'NOK': 0,
#         'INR': 0,
#         'PHP': 0
#         }
#     for k in base_code.keys() :
#         url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={}&to_symbol=JPY&apikey={}'.format(k, key)
#         rq = requests.get(url)
#         data = rq.json()
#         base_code[k] = float(data["Time Series FX (Daily)"][date[0]]["4. close"])
#     return base_code


# 下記はあくまで一例
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

        # ここに関数定義

        def sql_write(base="JPY", period="today", rate_dic={}):

        # paymentとrateは渡された辞書型配列のものを入れる
        # payment="USD"
        # rate=0.0072050764
            [year, month, day] = datetime.fromtimestamp(today_ut).strftime("%Y-%m-%d").split('-')
            # [year, month, day] = datetime.fromtimestamp(today_ut).strftime("%Y-%m-%d").split('-')

            updated_val = '-'.join([year, month, day])

    
            for k, v in rate_dic.items():

                # [TODO]スケジューラーに上げるときはUPDATEに変更すること
                # SQL文の文字列はシングルクォートでなければエラーが出る
                convert_v = float(v)

                # [重要]yeasterdayの分が終わったらupdateの方をコメントアウトを解除する
                # cursor.execute(f"INSERT INTO rate(base_code, payment_code, rate_val, rate_period, updated) VALUES (\'{base}\', \'{k}\', {v}, \'{period}\', \'{updated_val}\')")
                # updatedにはシングルクォートを忘れないこと
                cursor.execute(f"UPDATE rate SET rate_val={v}, updated=\'{updated_val}\' WHERE base_code=\'{base}\' AND payment_code=\'{k}\' AND rate_period=\'{period}\'")

            
            # 引数に辞書型配列を格納できるように
            # UPDATEでも代用が効くように

        # sql = "INSERT INTO todo (task) VALUES ('hello')"
        # cursor.execute(sql)

        # sql_write(period="last_week", rate_dic=weeks_test)
        # todayの分
        sql_write(rate_dic=today_jpy_XXX_rate);


    connection.commit()