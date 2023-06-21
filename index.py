from forex_python.converter import CurrencyRates
from datetime import datetime

# 取得するのは現在、昨日、先週(週の頭からケツまでの平均)、先月(月の頭からケツまでの平均)、一年前(1/1～12/31の平均)(場合によっては三、五、十年前も)
# 年単位のレートはあらかじめデータベースに手動で入れておいた方が楽

# datetimeで取った日付よりもunix時間の数値の方がいいかもしれない
# どちらをつかうにせよ 年月日時分の5つの数値が取得できればいい
# datetime型で想定すると 型をstringに直して分解して配列にする → それぞれ対応した変数へ格納する
# うるう年は2月29日がある
# 30日なのは4，6，9，11の月 
# 31日なのは1，3，5，7，8，10，12の月 
# 28日(うるう年は29日)なのは2月

# 日時を指定しなければ0時0分になる
# date_test = datetime(2020, 5, 4)
# print(date_test)


# 通貨（日本円の場合: JPYと指定）
currency = 'JPY'

currencysec = 'USD'

# 実行
obj = CurrencyRates()
# 年月日を指定しなければ現在のレートを取得
values = obj.get_rates(currency)
print(values)



# 今日の日付
date_today = datetime.today()
today_str_type = date_today.strftime("%Y-%m-%d").split('-')
# datetime型から文字列に変換 → 年月日に分割
[year, month, day] = today_str_type

# 各年月日よりも1少ない日付からレートを取ってみる
past_date = datetime(int(year) - 1, int(month) - 1, int(day) - 1)

# 取得したいのは USD(アメリカドル) EUR(ユーロ) GBP(イギリスポンド) CHF(スイスフラン) AUD(オーストラリアドル) KRW(韓国ウォン) CNY(中国元)

past_rate = obj.get_rates(currency, past_date)
# 帰ってくるのは辞書型だからキーを指定(取り出す際に指定した方が良いかも)
# いちいち取り出すのが面倒なので後で関数を作る
my_past_rate = {
    'USD': past_rate['USD'],
    'EUR': past_rate['EUR'],
    'GBP': past_rate['GBP'],
    'CHF': past_rate['CHF'],
    'AUD': past_rate['AUD'],
    'KRW': past_rate['KRW'],
    'CNY': past_rate['CNY']
    }

print(my_past_rate)
