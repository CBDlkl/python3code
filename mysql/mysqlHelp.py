import pymysql


class mysql_help:
    def __init__(self):
        print("基于pymysql的mysql操作初始化...")

    mysqlInfo = {
        "host": "172.16.5.15",
        "port": 3306,
        "user": "zhang",
        "passwd": "zhang",
        "db": "fasttrave",
        "charset": "utf8"
    }

    def Open(self):
        conn = pymysql.connect(
            host=self.mysqlInfo["host"],
            port=self.mysqlInfo["port"],
            user=self.mysqlInfo["user"],
            passwd=self.mysqlInfo["passwd"],
            db=self.mysqlInfo["db"],
            charset=self.mysqlInfo["charset"]
        )
        return {"cur": conn.cursor(), "conn": conn}

    def Close(self, cur, conn):
        cur.close()
        conn.commit()
        conn.close()

    def GetSingel(self, sql, tuples):
        open = self.Open()
        cur = open["cur"]
        conn = open["conn"]

        try:
            count = cur.execute(sql, tuples)
            # list = cur.fetchall()
            list = cur.fetchone()

        except pymysql.Error as e:
            print("数据库操作发生异常:", e)
        self.Close(cur=cur, conn=conn)

        return list

    def GetAll(self, sql, tuples):
        open = self.Open()
        cur = open["cur"]
        conn = open["conn"]

        try:
            count = cur.execute(sql, tuples)
            list = cur.fetchall()

        except pymysql.Error as e:
            print("数据库操作发生异常:", e)
        self.Close(cur=cur, conn=conn)

        return list

    def InsertOrUpdate(self, sql, tuples):
        open = self.Open()
        cur = open["cur"]
        conn = open["conn"]

        try:
            count = cur.execute(sql, tuples)
        except pymysql.Error as e:
            print("数据库操作发生异常:", e)
        self.Close(cur=cur, conn=conn)

        return count

    # 返回自增长ID
    def InsertOutId(self, sql, tuples):
        open = self.Open()
        cur = open["cur"]
        conn = open["conn"]

        try:
            count = cur.execute(sql, tuples)
            cur.execute("SELECT LAST_INSERT_ID()")
            autoid = cur.fetchone()[0]
        except pymysql.Error as e:
            print("数据库操作发生异常:", e)
        self.Close(cur=cur, conn=conn)

        return autoid
