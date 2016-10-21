import pymysql


class mysql_help:
    isAutoClose = True

    def __init__(self, isAutoClose=True):
        self.isAutoClose = isAutoClose
        # print("基于pymysql的mysql操作初始化")

    mysqlInfo = {
        "host": "172.16.5.15",
        "port": 3306,
        "user": "zhang",
        "passwd": "zhang",
        "db": "fasttrave",
        "charset": "utf8"
    }

    conn = None
    cur = None

    def Open(self):
        if self.conn is not None:
            return
        self.conn = pymysql.connect(
            host=self.mysqlInfo["host"],
            port=self.mysqlInfo["port"],
            user=self.mysqlInfo["user"],
            passwd=self.mysqlInfo["passwd"],
            db=self.mysqlInfo["db"],
            charset=self.mysqlInfo["charset"]
        )
        self.cur = self.conn.cursor()

    def Close(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def GetSingel(self, sql, tuples):
        self.Open()

        try:
            count = self.cur.execute(sql, tuples)
            # list = cur.fetchall()
            list = self.cur.fetchone()

        except pymysql.Error as e:
            print("数据库操作发生异常:", e)
        if self.isAutoClose:
            self.Close()
        return list

    def GetAll(self, sql, tuples=()):
        self.Open()

        try:
            count = self.cur.execute(sql, tuples)
            list = self.cur.fetchall()

        except pymysql.Error as e:
            print("数据库操作发生异常:", e)
        if self.isAutoClose:
            self.Close()
        return list

    def InsertOrUpdate(self, sql, tuples):
        self.Open()

        try:
            count = self.cur.execute(sql, tuples)
        except pymysql.Error as e:
            print("数据库操作发生异常:", e)
        if self.isAutoClose:
            self.Close()

        return count

    # 返回自增长ID
    def InsertOutId(self, sql, tuples):
        self.Open()

        try:
            count = self.cur.execute(sql, tuples)
            self.cur.execute("SELECT LAST_INSERT_ID()")
            autoid = self.cur.fetchone()[0]
        except pymysql.Error as e:
            print("数据库操作发生异常:", e)
        if self.isAutoClose:
            self.Close()
        return autoid
