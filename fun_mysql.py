import pymysql


class AccessToMysql(object):
    # 初始化参数
    def __init__(self, host, user, passwd, database):
        # self.conn = pymysql.connect(
        #     host=host,
        #     user=user,
        #     password=passwd,
        #     database=database,
        #     charset='utf8',
        #     cursorclass=pymysql.cursors.DictCursor)
        # self.cursor = self.conn.cursor()
        self.conn = None
        self.cursor = None
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

    def __connect_to_mysql(self):  # 连接数据库
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.passwd,
            database=self.database,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def execute_sql(self, sql):  # 执行sql语句,用于创建table,和显示数据
        self.__connect_to_mysql()
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交执行
            self.conn.commit()
        except Exception as e:
            # 如果执行sql语句出现问题，则执行回滚操作
            self.conn.rollback()
            if "Duplicate entry" in str(e):
                print("Duplicate action? Roll Back!")
            else:
                print(e)
        finally:
            self.disconnect()

    def fetch(self):
        try:
            self.__connect_to_mysql()
            content = self.cursor.fetchall()
        except Exception as e:
            raise e
        else:
            print(content)
            self.disconnect()

    def disconnect(self):
        self.cursor.close()
        self.conn.close()
