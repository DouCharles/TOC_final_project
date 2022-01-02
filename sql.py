import pymysql

db_settings = {
    "host" : "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "ddcharles",
    "db": "toc",
    "charset": "utf8mb4"
}

def sql_search_memo():
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            command = "select * from toc.memo"
            cursor.execute(command)
            result = cursor.fetchall()
            print(result)
            return(result)

    except Exception as ex:
        print(ex)

def sql_search_account(cost_income):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            command = "select * from toc.account where cost_income = %s"
            cursor.execute(command,(cost_income))
            result = cursor.fetchall()
            print(result)
            return(result)

    except Exception as ex:
        print(ex)

def sql_delete_memo(id):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        print("type = ",type(id))
        print(id)
        with conn.cursor() as cursor:
            command = "delete from toc.memo where id = %s"
            cursor.execute(command,(id))
            conn.commit()
            command = "select * from toc.memo"
            cursor.execute(command)
            result = cursor.fetchall()
            print(result)
    except Exception as ex:
        print(ex)

def sql_insert_memo(content,time):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "insert into toc.memo(time, content) values(%s,%s)"
            cursor.execute(command,(time,content))
            conn.commit()
            command = "select * from toc.memo"
            cursor.execute(command)
            result = cursor.fetchall()
            print(result)

    except Exception as ex:
        print(ex)

def sql_insert_account(content,money,cost_income):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            command = "insert into toc.account(money,content,cost_income) values(%s,%s,%s)"
            cursor.execute(command,(money,content,cost_income))
            conn.commit()
            command = "select * from toc.account"
            cursor.execute(command)
            result = cursor.fetchall()
            print(result)

    except Exception as ex:
        print(ex)

def sql_reset():

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            command = "TRUNCATE TABLE toc.memo"
            cursor.execute(command)
            conn.commit()
            command = "TRUNCATE TABLE toc.account"
            cursor.execute(command)
            conn.commit()
            # command = "select * from toc.memo"
            # cursor.execute(command)
            # result = cursor.fetchall()
            # print(result)

    except Exception as ex:
        print(ex)

def sql_delete_account(id):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            command = "delete from toc.account where idaccount = %s"
            cursor.execute(command,id)
            conn.commit()

    except Exception as ex:
        print(ex)