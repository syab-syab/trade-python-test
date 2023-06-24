from forex_python.converter import CurrencyRates
import time
from datetime import datetime
import statistics
from calendar import isleap

# 試しに先週の JPY/USDの平均を算出する

currency = 'JPY'

obj = CurrencyRates()

# まず今日のunix時間を取得
today_ut = time.time()

today_stamp = datetime.fromtimestamp(today_ut)
print(f"今日は{today_stamp}")

rates = obj.get_rates(currency, today_stamp)
print(f"今日のJPY/USDは{rates['USD']}")

#　unix時間から一週間分の日付を算出
# 一週分のレートの平均を出す
def last_weeks_rates(uni):
    week_id = [1, 2, 3, 4, 5, 6, 7]
    rates = []
    for i in week_id:
        tmp = uni - (86400 * i)
        day_stamp = datetime.fromtimestamp(tmp)
        day_rate = obj.get_rates(currency, day_stamp)
        # print(day_stamp)
        # print(day_rate['USD'])
        rates.append(day_rate['USD'])
    # 一週分の平均を返す
    return statistics.mean(rates)


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
    return [modified_year, modified_month, number_of_days]



weeks_test = last_weeks_rates(today_ut)
print(weeks_test)
months_test = last_months_rates(today_ut)
print(months_test)

testing = last_months_rates(1047567600.0)
print(testing)

# レートは小数点以下四桁までで四捨五入した方が良いかも