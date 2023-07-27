import psycopg2

# pass = 'tset-esabatad-database-test'
# port = 5432


# 接続情報

# コネクション
connection = psycopg2.connect(
    dbname='unknown',
    host='unknown',
    user='unknown',
    port=0000,
    password='unknown'
)

with connection:
    with connection.cursor() as cursor:
        sql = "INSERT INTO todos (task) VALUES ('hello world')"
        cursor.execute(sql)
    connection.commit()



# コネクション等は閉じる。
# cur.close()
# conn.close();