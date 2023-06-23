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

    # うるう年かどうかチェック
    detect_leap = isleap(int(year))


    # monthが2, 4, 6, 9, 11の月は30日間でfalse
    # 1, 3, 5, 7, 8, 10, 12の月はture
    # is_month = any([1, 3, 5, 7, 8, 10, 12])

    # そうでない月は31日間のレートの平均を出す
    # 2月のみ28日間でうるう年の時は29日間
    # もし一月なら先月である12月は去年となる
    if month == 2 or month == 4 or month == 9 or month == 11 :
        number_of_days = 30
    else:
        number_of_days = 31
    return detect_leap



weeks_test = last_weeks_rates(today_ut)
print(weeks_test)
months_test = last_months_rates(today_ut)
print(months_test)

# レートは小数点以下四桁までで四捨五入した方が良いかも