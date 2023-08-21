import psycopg2


# stateテーブルの更新テスト
connection = psycopg2.connect(
    # dbname='unKnown',
    # host='unKnown',
    # user='unKnown',
    # port=0000,
    # password="unKnown",
    dbname='postgres',
    host='db.mwbijuaheftllmpuwmtt.supabase.co',
    user='postgres',
    port=5432,
    password="0hXrktyaBb74IURE"

)

with connection:
    with connection.cursor() as cursor:
        sql = "INSERT INTO state(state, tag) VALUES ('1', 'state management')"
        # ↑をupdate文にする
        cursor.execute(sql)
        # selectで取得した値をprintする
        # cursor.execute(sql)
    connection.commit()