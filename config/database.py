import pymysql

def connect_db():
    try:
        conn = pymysql.connect(host="localhost",
                               user="root",
                               password="root",
                               charset='utf8mb4',
                               db="vue_crud",
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
