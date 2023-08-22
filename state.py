import psycopg2




def test():
    # stateテーブルの更新テスト
    connection = psycopg2.connect(
        dbname='unKnown',
        host='unKnown',
        user='unKnown',
        port=0000,
        password="unKnown",
    )

    # 関数でwith文を囲っても大丈夫っぽい
    with connection:
        with connection.cursor() as cursor:
            # sql = "INSERT INTO state(state, tag) VALUES ('1', 'state management')"
            update ="UPDATE state SET state = '1' WHERE id = 1"
            # ↑をupdate文にする
            # cursor.execute(sql)
            cursor.execute(update)
            # selectで取得した値をprintする
            select = "SELECT state FROM state WHERE id = 1"
            cursor.execute(select)
            row = cursor.fetchone()
            print(row[0])
            print(row[0] == '1')
            # cursor.execute(sql)
        connection.commit()

test()