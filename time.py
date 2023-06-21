import time
from datetime import datetime

# unix時間からdatetimeを算出
ut = time.time()

print(ut)

date_ut = datetime.fromtimestamp(ut)

print(date_ut)

# 24時間 = 86400秒
# 算出したunix時間に足したり引いたりすれば～日後・前を表せる
date_test = datetime.fromtimestamp(ut - 86400.00)

print(date_test)