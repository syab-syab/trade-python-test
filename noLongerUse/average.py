from forex_python.converter import CurrencyRates
import time
from datetime import datetime
import statistics
from calendar import isleap
import psycopg2


# 取得したいのは
# USD(アメリカドル), EUR(ユーロ), GBP(イギリスポンド), CHF(スイスフラン)
# AUD(オーストラリアドル), KRW(韓国ウォン), CNY(中国元)
# 今後増やすかも
# 追加するのは
# IDR(インドネシア)、CAD(カナダ)、MYR(マレーシア)、SGD(シンガポール)、
# HKD(香港)、NZD(ニュージーランド)、THB(タイ)、
# NOK(ノルウェー)、INR(インド)、PHP(フィリピン)

# JPY/USDの平均を算出する
# 全関数共通の変数
currency = 'JPY'

obj = CurrencyRates()

# まず今日のunix時間を取得
today_ut = time.time()

def format_ut(value):
    return datetime.fromtimestamp(value)

# 今日の分のレート
# datetime型を引数にとっても良かったけど
# 何となく他の関数と統一した方が万が一の混乱は避けられるかもしれないと思った
def one_day_rate(uni) :
    # today_stamp = datetime.fromtimestamp(uni)
    one_day_stamp = format_ut(uni)
    # [TODO]将来的に使えなくなるコードが出てくるかもしれないので(RUBのように)
    # その際のエラー処理を書く
    one_day_rates = {
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
    # わざわざfor文で回すのが無駄すぎた
    origin_value = obj.get_rates(currency, one_day_stamp)
    for k in one_day_rates.keys() :
        one_day_rates[k] = origin_value[k]
        # print(k + ': ' + str(today_rates[k]))
    return one_day_rates

# 保留
# 〇〇〇 / JPYのレートを取得(今日の分のみ)
# def today_rate_jpy(uni) :
#     today_stamp = datetime.fromtimestamp(uni)
#     today_rates_jpy = {
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
#     for k in today_rates_jpy.keys() :
#         today_rates_jpy[k] = obj.get_rates(k, today_stamp)['JPY']
#     return today_rates_jpy

# 月と週のレート取得共通の関数
# target_timeはunix時間
def fetch_several_rates(start_val, end_val, target_time) :

    # 返すためのレートの辞書型配列を用意する
    # [TODO]将来的に使えなくなるコードが出てくるかもしれないので(RUBのように)
    # その際のエラー処理を書く

    ave_rates = {
    'USD': [],
    'EUR': [],
    'GBP': [],
    'CHF': [],
    'AUD': [],
    'KRW': [],
    'CNY': [],
    'IDR': [],
    'CAD': [],
    'MYR': [],
    'SGD': [],
    'HKD': [],
    'NZD': [],
    'THB': [],
    'NOK': [],
    'INR': [],
    'PHP': []
    }

    # レートの取得
    # end_valには週の場合8を代入する
    for i in range(start_val, end_val) :
        tmp_date = 0
        if end_val == 8 :
            tmp_date = target_time - (86400 * i)
        else :
            tmp_date = target_time + (86400 * i)
        # day_stamp = datetime.fromtimestamp(tmp_date)
        day_stamp = format_ut(tmp_date)
        # day_rateに一日のレートがすべて入っている
        day_rate = obj.get_rates(currency, day_stamp)
        # 取得したレートをあらかじめ用意しておいた辞書型配列に
        # キー毎に格納していく
        for k in ave_rates.keys() :
            ave_rates[k].append(day_rate[k])
    
    # 各キーに格納した配列の平均を格納していく
    for k in ave_rates.keys() :
        ave_rates[k] = statistics.mean(ave_rates[k])
    
    return ave_rates



#　unix時間から一週間分の日付を算出
# 一週分のレートの平均を出す
def last_weeks_rates(uni):
    # rangeの仕様上終点を8に
    # 関数fetch_rateの返り値を返す
    return fetch_several_rates(1, 8, uni)


# 先月分のレートの平均を算出する
def last_months_rates(uni):
    # tmp = datetime.fromtimestamp(uni)
    tmp = format_ut(uni)
    [year, month, day] = tmp.strftime("%Y-%m-%d").split('-')

    # 取得する先月の日数
    number_of_days = 0

    # 取得する月(今月から1を引いた数)
    # ただし、1月の場合0になってしまうので12に戻す
    modified_month = int(month) - 1

    # 取得する月の年
    modified_year = int(year)

    # うるう年かどうかチェック
    detect_leap = isleap(modified_year)

    # 取得した月 - 1 の月だから
    # 例えば、2, 4, 6, 9, 11 なら number_of_daysは31になる
    if  modified_month == 4 or modified_month == 6 or modified_month == 9 or modified_month == 11 :
        number_of_days = 30
    elif modified_month == 2 :
        # うるう年なら29日間にする
        if detect_leap :
            number_of_days = 29
        # 違うなら28日間
        else :
            number_of_days = 28
    else:
        number_of_days = 31
        # もし1月なら先月である12月は去年となる
        if modified_month == 0 :
            modified_year -= 1
            # 月を12に戻す
            modified_month = 12

    # range関数にmodified_yearとmodified_monthを使って
    # レートを取得する

    # 共通の関数を使うため先月の一日目のunix時間を取得する
    last_months_first_day = datetime(modified_year, modified_month, 1).timestamp()

    # 関数fetch_rateの返り値を返す
    return fetch_several_rates(0, number_of_days, last_months_first_day)


# 今日の分のレートを格納
today_test = one_day_rate(today_ut)

# 昨日の分のレートを格納
yesterday_test = one_day_rate(today_ut - 86400.00)

# 先週の分(平均)のレートを格納
weeks_test = last_weeks_rates(today_ut)

# 先月の分(平均)のレートを格納
months_test = last_months_rates(today_ut)

# 今日、先週、先月に格納し終えてから
# データベースへUPDATEする(レート取得をすべて済ませてから)

# [TODO]○○/jpyの精度が低かったのでデータベースへの格納は一旦保留
# def sql_jpy_write(rate_dic={}):
#     for k, v in rate_dic.items():
#         print(f"INSERT INTO rate(base_code, payment_code, rate_val, rate_period) VALUES (\'{k}\', 'JPY', {v}, 'today')")

# sql_jpy_write(today_jpy_test)

# 下記はあくまで一例
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

        # ここに関数定義

        def sql_write(base="JPY", period="today", rate_dic={}):

        # paymentとrateは渡された辞書型配列のものを入れる
        # payment="USD"
        # rate=0.0072050764
            [year, month, day] = format_ut(today_ut).strftime("%Y-%m-%d").split('-')
            # [year, month, day] = datetime.fromtimestamp(today_ut).strftime("%Y-%m-%d").split('-')

            updated_val = '-'.join([year, month, day])
            # print(updated_val)
            # print(type(updated_val))
    
            for k, v in rate_dic.items():

                # [TODO]スケジューラーに上げるときはUPDATEに変更すること
                # SQL文の文字列はシングルクォートでなければエラーが出る

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
        sql_write(rate_dic=today_test);

        # yesterdayの分
        sql_write(period="yesterday", rate_dic=yesterday_test)

        # last_weekの分
        sql_write(period="last_week", rate_dic=weeks_test)

        # last_monthの分
        sql_write(period="last_month", rate_dic=months_test)


    connection.commit()