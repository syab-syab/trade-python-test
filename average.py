from forex_python.converter import CurrencyRates
import time
from datetime import datetime
import statistics
from calendar import isleap


# 取得したいのは
# USD(アメリカドル), EUR(ユーロ), GBP(イギリスポンド), CHF(スイスフラン)
# AUD(オーストラリアドル), KRW(韓国ウォン), CNY(中国元)
# 今後増やすかも

# JPY/USDの平均を算出する
# 全関数共通の変数
currency = 'JPY'

obj = CurrencyRates()

# まず今日のunix時間を取得
today_ut = time.time()

# 今日の分のレート
# datetime型を引数にとっても良かったけど
# 何となく他の関数と統一した方が万が一の混乱は避けられるかもしれないと思った
def today_rate(uni) :
    today_stamp = datetime.fromtimestamp(uni)
    rate = obj.get_rates(currency, today_stamp)
    rate_usd = rate['USD']
    rate_eur = rate['EUR']
    rate_gbp = rate['GBP']
    rate_chf = rate['CHF']
    rate_aud = rate['AUD']
    rate_krw = rate['KRW']
    rate_cny = rate['CNY']
    today_rates = {
        'USD': rate_usd,
        'EUR': rate_eur,
        'GBP': rate_gbp,
        'CHF': rate_chf,
        'AUD': rate_aud,
        'KRW': rate_krw,
        'CNY': rate_cny
        }
    return today_rates

# 〇〇〇 / JPYのレートを取得(今日の分のみ)
def today_rate_jpy(uni) :
    today_stamp = datetime.fromtimestamp(uni)
    # 下の処理はfor文で回した方が良いかも
    rate_usd = obj.get_rates('USD', today_stamp)
    rate_eur = obj.get_rates('EUR', today_stamp)
    rate_gbp = obj.get_rates('GBP', today_stamp)
    rate_chf = obj.get_rates('CHF', today_stamp)
    rate_aud = obj.get_rates('AUD', today_stamp)
    rate_krw = obj.get_rates('KRW', today_stamp)
    rate_cny = obj.get_rates('CNY', today_stamp)
    today_rates_jpy = {
        'USD/JPY': rate_usd['JPY'],
        'EUR/JPY': rate_eur['JPY'],
        'GBP/JPY': rate_gbp['JPY'],
        'CHF/JPY': rate_chf['JPY'],
        'AUD/JPY': rate_aud['JPY'],
        'KRW/JPY': rate_krw['JPY'],
        'CNY/JPY': rate_cny['JPY']
        }
    return today_rates_jpy

# 月と週のレート取得共通の関数
# target_timeはunix時間
def fetch_rates(start_val, end_val, target_time) :

    # 返すためのレートの辞書型配列を用意する
    ave_rates = {
    'USD': [],
    'EUR': [],
    'GBP': [],
    'CHF': [],
    'AUD': [],
    'KRW': [],
    'CNY': []
    }

    # レートの取得
    # end_valには週の場合8を代入する
    for i in range(start_val, end_val) :
        tmp_date = 0
        if end_val == 8 :
            tmp_date = target_time - (86400 * i)
        else :
            tmp_date = target_time + (86400 * i)
        day_stamp = datetime.fromtimestamp(tmp_date)
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
    return fetch_rates(1, 8, uni)


# 先月分のレートの平均を算出する
def last_months_rates(uni):
    tmp = datetime.fromtimestamp(uni)
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
    return fetch_rates(0, number_of_days, last_months_first_day)


today_test = today_rate(today_ut)
print(today_test)
today_jpy_test = today_rate_jpy(today_ut)
print(today_jpy_test)
weeks_test = last_weeks_rates(today_ut)
print(weeks_test)
months_test = last_months_rates(today_ut)
print(months_test)

# レートは小数点以下四桁までで四捨五入した方が良いかも