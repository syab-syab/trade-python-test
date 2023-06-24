import time
from datetime import datetime
from calendar import isleap

# unix時間からdatetimeを算出
ut = time.time()

print(ut)

date_ut = datetime.fromtimestamp(ut)

print(date_ut)

# 24時間 = 86400秒
# 算出したunix時間に足したり引いたりすれば～日後・前を表せる
date_test = datetime.fromtimestamp(ut - 86400.00)

print(date_test)

[year, month, day] = datetime(2023, 10, 3).strftime("%Y-%m-%d").split('-')
test_month = int(month)
print(type(test_month))
print(test_month)

def urudoshi(years):
    result = isleap(years)
    if result:
        return "うるう年です"
    else:
        return "うるう年違います"
    
print(urudoshi(2100))
testing = datetime(2003, 3, 14)
print(testing.timestamp())