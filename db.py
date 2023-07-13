import psycopg2

# pass = 'tset-esabatad-database-test'
# port = 5432


# 接続情報
# dsn = "dbname=postgres host=db.ncddhgoemdbghyzcmvmg.supabase.co user=postgres port=5432 password=tset-esabatad-database-test"

# コネクション
# conn = psycopg2.connect(dsn)  
connection = psycopg2.connect(
    dbname='postgres',
    host='db.ncddhgoemdbghyzcmvmg.supabase.co',
    user='postgres',
    port=5432,
    password='tset-esabatad-database-test'
)

with connection:
    with connection.cursor() as cursor:
        sql = "INSERT INTO todos (task) VALUES ('hello')"
        cursor.execute(sql)
    connection.commit()



# コネクション等は閉じる。
# cur.close()
# conn.close();