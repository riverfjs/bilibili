import pymysql
from DBUtils.PooledDB import PooledDB
import constants


class Database:
    def __init__(self, *db):
        # mysql数据库
        self.host = constants.mysqlInfo['host']
        self.port = constants.mysqlInfo['port']
        self.user = constants.mysqlInfo['user']
        self.pwd = constants.mysqlInfo['passwd']
        self.db = constants.mysqlInfo['db']
        self.charset = constants.mysqlInfo['charset']
        self.limit = constants.limit_count
        self._CreatePool()

    def _CreatePool(self):

        self.Pool = PooledDB(creator=pymysql, mincached=self.limit, blocking=True,
                             host=self.host, port=self.port,
                             user=self.user, password=self.pwd, database=self.db, charset=self.charset)

    def _Getconnect(self):
        try:
            self.conn = self.Pool.connection()
            cur = self.conn.cursor()
        except Exception as e:
            print(e)
        else:
            if not cur:
                raise NameError
            else:
                return cur

    # 查询sql
    def ExecQuery(self, sql):
        try:
            cur = self._Getconnect()
            cur.execute(sql)
        except Exception  as err:
            print(err)
        else:
            relist = cur.fetchall()
            cur.close()
            self.conn.close()
            return relist

    # 非查询的sql,增删改
    def ExecNoQuery(self, sql):
        cur = self._Getconnect()
        try:
            cur.execute(sql)
            self.conn.commit()
            ret = {'result': True, 'id': int(cur.lastrowid)}
        except Exception as e:
            self.conn.rollback()
            ret = {'result': False, 'err': e}
        finally:
            cur.close()
            self.conn.close()

    # 显示查询中的第一条记录
    def Showfirst(self, sql):
        try:
            cur = self._Getconnect()
            cur.execute(sql)
        except Exception as err:
            print(err)
        else:
            resultfirst = cur.fetchone()
            cur.close()
            self.conn.close()
            return resultfirst

    # 显示查询出的所有结果
    def Showall(self, sql):
        cur = self._Getconnect()
        cur.execute(sql)
        resultall = cur.fetchall()
        cur.close()
        self.conn.close()
        return print(resultall)



