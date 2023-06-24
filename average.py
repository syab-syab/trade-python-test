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
    rates = []
    for i in range(1, 8):
        tmp = uni - (86400 * i)
        day_stamp = datetime.fromtimestamp(tmp)
        day_rate = obj.get_rates(currency, day_stamp)
        # print(day_stamp)
        # print(day_rate['USD'])
        # 便宜上USDのみだが本番は他の値も取得する
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
    rates = []
    # rangeの仕様上number_of_timeを1増やす
    for i in range(1, (number_of_days + 1)):
        last_months_day_stamp = datetime(modified_year, modified_month, i)
        print(last_months_day_stamp)
        day_rate = obj.get_rates(currency, last_months_day_stamp)
        rates.append(day_rate['USD'])

    # 先月分の平均を返す
    return statistics.mean(rates)
    # return [modified_year, modified_month, number_of_days]



weeks_test = last_weeks_rates(today_ut)
print(weeks_test)
months_test = last_months_rates(today_ut)
print(months_test)

# レートは小数点以下四桁までで四捨五入した方が良いかも