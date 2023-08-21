# supabaseのデータのアップデート
# まだ仮組みの未完成
import requests
from datetime import datetime
import time
import psycopg2

def update_rates():
    # supabaseへの接続パス
    connection = psycopg2.connect(
      dbname='unKnown',
      host='unKnown',
      user='unKnown',
      port=0000,
      password="unKnown",
    )

    # 全ての処理はwith以下でやった方が良さそう
    with connection:
        with connection.cursor() as cursor:
            # stateテーブルのid:1の値を取得
            select = "SELECT state FROM state WHERE id = 1"
            cursor.execute(select)
            state = cursor.fetchone()
            print(state[0])
            print(state[0] == '1')

            # unix時間からdatetimeを算出
            today_ut = time.time()
            
            # apiのキーを忘れずに
            api_key = 'XXXX'

            # stateテーブルの値で返す辞書型の内容を変更する
            def create_payment_code(state):
                if state == '1':
                    return { 'USD': [], 'AUD': [], 'CAD': [], 'TWD': [], 'CNY': [] }
                elif state == '2':
                    return { 'EUR': [], 'GBP': [], 'CHF': [], 'THB': [], 'SGD': [] }
                elif state == '3':
                    return { 'MYR': [], 'NOK': [], 'INR': [], 'PHP': [], 'KRW': [] }
                else:
                    return { 'USD': [], 'AUD': [], 'CAD': [], 'TWD': [], 'CNY': [] }

            def today_rate(key, state) :
                payment_code = create_payment_code(state)

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
                
            jpy_otr_rate = today_rate(api_key, state[0])

            def sql_write(base="JPY", rate_dic={}):
                [year, month, day] = datetime.fromtimestamp(today_ut).strftime("%Y-%m-%d").split('-')
                updated_val = '-'.join([year, month, day])
                for k, v in rate_dic.items():
                    # /updatedにはシングルクォートを忘れないこと
                    # v[0], v[1]
                    cursor.execute(f"UPDATE rate SET rate_dates=\'{v[0]}\' ,rate_val=\'{v[1]}\', updated=\'{updated_val}\' WHERE base_code=\'{base}\' AND payment_code=\'{k}\'")
            
            # todayの分
            sql_write(rate_dic=jpy_otr_rate)

            # stateテーブルの値をアップデート
            # 全ての処理が終わったらstateテーブルの値を更新する
            if state == '1':
                cursor.execute("UPDATE state SET state = '2' WHERE id = 1")
            elif state == '2':
                cursor.execute("UPDATE state SET state = '3' WHERE id = 1")
            elif state == '3':
                cursor.execute("UPDATE state SET state = '1' WHERE id = 1")
            else:
                cursor.execute("UPDATE state SET state = '1' WHERE id = 1")
            # ↑をupdate文にする

        connection.commit()

update_rates()

# gcp用にif文を用いた新たな関数を下に書いてupdate_ratesを実行できるようにエンドポイントにする