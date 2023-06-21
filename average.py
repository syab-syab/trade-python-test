from forex_python.converter import CurrencyRates
import time
from datetime import datetime

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

def weekly_rates(uni):
    week_id = [1, 2, 3, 4, 5, 6, 7]
    rates = []
    for i in week_id:
        tmp = uni - (86400 * i)
        day_stamp = datetime.fromtimestamp(tmp)
        day_rate = obj.get_rates(currency, day_stamp)
        print(day_stamp)
        print(day_rate['USD'])
        rates.append(day_rate['USD'])
    return rates

test = weekly_rates(today_ut)
print(test)