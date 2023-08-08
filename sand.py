from datetime import datetime, timezone
import time

# utc
now = datetime.now(timezone.utc)
print(now)
print(now.timestamp())

# jtc
jst = datetime.now()
print(jst)
print(jst.timestamp())

today_ut = time.time()
print(today_ut)
# tz=timezone.utcのオプションを付けることでutc時間にできる
print(datetime.fromtimestamp(today_ut, tz=timezone.utc))

# now_str_type = now.strftime("%Y-%m-%d").split('-')
# [year, month, day] = now_str_type
# print([year, month, day])