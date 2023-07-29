import time
from datetime import datetime
from calendar import isleap

# unix時間からdatetimeを算出
ut = time.time()

# print(ut)

# date_ut = datetime.fromtimestamp(ut)

# print(date_ut)
# print(str(date_ut))

# 24時間 = 86400秒
# 算出したunix時間に足したり引いたりすれば～日後・前を表せる
date_test = datetime.fromtimestamp(ut - 86400.00)

print(date_test)

# [year, month, day] = datetime(2023, 10, 3).strftime("%Y-%m-%d").split('-')
[year, month, day] = datetime.fromtimestamp(ut).strftime("%Y-%m-%d")
# ymd_tmp = datetime.fromtimestamp(ut).strftime("%Y-%m-%d").split('-')

test_month = '-'.join([year, month, day])
print(type(test_month))
print(test_month)

# def urudoshi(years):
#     result = isleap(years)
#     if result:
#         return "うるう年です"
#     else:
#         return "うるう年違います"
    
# print(urudoshi(2100))
# testing = datetime(2003, 3, 14)
# print(type(testing.timestamp()))
# tests = datetime(2023, 5, 1).timestamp()
# print(type(tests))

# print(type(ut))

# tes_arr = {'one': 1, 'two': 2, 'three': 3}
# for k, v in tes_arr.items() :
#     tes_arr[k] = 1
#     print(tes_arr[k])
# print(tes_arr)

# usdの平均→ 0.006984086242299794

# usd_w = [0.006984086242299794, 0.006984086242299794, 0.006984086242299794, 0.006984086242299794, 0.006984086242299794, 0.006984086242299794, 0.006984086242299794]
# print(len(usd_w))
# usd_m = [0.007167169179229481, 0.00720125786163522, 0.00720125786163522, 0.00720125786163522, 0.007128567618031475, 0.007165470521161715, 0.007172399946459645, 0.007158954527270304, 0.007175186368477103, 0.007175186368477103, 0.007175186368477103, 0.007175186368477103, 0.007175231620342598, 0.007165715044482803, 0.007148336750214933, 0.007148336750214933, 0.007090850307145166, 0.007090850307145166, 0.007090850307145166, 0.007090850307145166, 0.007075917416348457, 0.007075917416348457, 0.007039410445370074, 0.006984086242299794, 0.006984086242299794, 0.006984086242299794, 0.006984086242299794, 0.006984086242299794, 0.006984086242299794, 0.006984086242299794]
# print(len(usd_m))

# test_dic = {'test': 0, 'test2' : 0}
# test_dic['test'] = 12345
# test_dic['test2'] = 6789
# print(test_dic)