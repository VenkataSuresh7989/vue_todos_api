import pymysql

def connect_db():
    try:
        conn = pymysql.connect(host="db4free.net",
                               user="vuecrud_7989",
                               password="Suresh@7989",
                               charset='utf8mb4',
                               db="vuecrud",
                               cursorclass=pymysql.cursors.DictCursor)
        return conn
    except Exception as e:
        print(str(e))

def disconnect_db(conn):
    try:
        if conn != None:
            conn.commit()
            conn.close()
    except Exception as e:
        print(str(e))
