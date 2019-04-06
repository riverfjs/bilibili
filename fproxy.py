import sys
import json
import random
from time import sleep
import telnetlib
import requests
from lxml import etree
from queue import Queue
from threading import Thread, currentThread, Lock
from scrapy.selector import Selector
from fun_mysql import AccessToMysql
from sqlpool import Database

overseasProxyUrl = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
internalProxyUrl = 'http://31f.cn/https-proxy/'
# proxyList = []


fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',  # noqa
}
internalSqls = []
overseasSqls = []
alltuples = []
sqlQueue = Queue()
lock = Lock()  # 全局锁用于数据库执行语句时加锁互斥线程


class ProxyPool(Database):
    sql1 = "CREATE TABLE if not exists test" \
           "(host char(20) PRIMARY KEY," \
           "port char(8)," \
           "type char(8))" \
           "DEFAULT charset='utf8mb4';"
    sql2 = "show tables;"

    def __init__(self):
        super(ProxyPool, self).__init__()
        self.queue = Queue()

    # def test(self):
    #     self.execute_sql(sql=self.sql2)
    #     self.fetch()
    #     self.disconnect()

    def getInternalProxy(self):
        response = requests.get(url=internalProxyUrl, headers=fake_headers)
        sel = Selector(response)
        proxies = sel.xpath('//table[@class="table table-striped"]//tr').extract()
        # print(proxies)
        for ii in proxies[1:14]:
            # print(ii)
            content = etree.HTML(ii)
            tmpList = (content.xpath('//td//text()'))
            # print(tmpList)
            host = tmpList[1]
            port = tmpList[2]
            proxyType = tmpList[6]
            # print(host, port, proxyType)
            hostType = "internal"
            proxiesTuple = (host, port, proxyType, hostType)
            alltuples.append(proxiesTuple)
            self.queue.put(proxiesTuple, block=True)
        print("ALL INTERNAL", len(alltuples))

    def getOverseasProxy(self):
        response = requests.get(url=overseasProxyUrl, headers=fake_headers)
        proxies_list = list(response.text.split('\n'))
        if not proxies_list[len(proxies_list) - 1]:
            proxies_list.pop()
        for proxy_str in proxies_list:
            try:
                proxy_json = json.loads(proxy_str)
            except Exception:
                print("Check json?", proxy_str)
            else:
                host = proxy_json['host']
                port = proxy_json['port']
                proxyType = proxy_json['type']
                # proxies = {'host': host, 'port': port, 'type': proxyType}
                hostType = 'overseas'
                proxiesTuple = (host, port, proxyType, hostType)
                alltuples.append(proxiesTuple)
                self.queue.put(proxiesTuple, block=True)
        print("ALL OVERSEAS", len(alltuples))

    def verify(self):
        proxiesTuple = self.queue.get(block=True)  # 不设置阻塞的话会一直去尝试获取资源
        try:
            telnet = telnetlib.Telnet(proxiesTuple[0], port=proxiesTuple[1], timeout=2)
        except Exception as e:
            print(proxiesTuple[0], ":", e)
            alltuples.remove(proxiesTuple)
        else:
            print(proxiesTuple[0], ":", "ok")
            if proxiesTuple[3] == 'overseas':  # 国内代理和国外代理分开写

                # with open('verified_overseas_proxies.json', 'a+') as f:
                #     f.write(proxiesJson + '\n')
                # print("已写入：%s" % proxies)
                sql = "INSERT INTO overseasproxy (host,port,type) VALUES {}".format(proxiesTuple[:-1])
                # sqlQueue.put(sql, block=True)
                lock.acquire(blocking=True)
                self.ExecNoQuery(sql)
                lock.release()
            else:

                # with open('verified_internal_proxies.json', 'a+') as f:
                #     f.write(proxiesJson + '\n')
                # print("已写入：%s" % proxies)
                sql = "INSERT INTO internalproxy (host,port,type) VALUES {}".format(proxiesTuple[:-1])
                # sqlQueue.put(sql, block=True)
                lock.acquire(blocking=True)
                self.ExecNoQuery(sql)
                lock.release()

    def insertData(self):
        sqlStatement = sqlQueue.get(block=True)
        self.ExecNoQuery(sqlStatement)

    def go(self):
        threads = []  # 待处理的线程
        for ii in alltuples:
            thread = Thread(target=self.verify)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()  # 同步线程
        print("SQLStatements all set!")

    def main(self):
        self.getOverseasProxy()
        # self.getInternalProxy()
        self.go()
        print(len(alltuples))
        # print("Total", len(overseasSqls), len(internalSqls))


def test():
    sys.stdout.write('Here are some codes.\r')
    sys.stdout.flush()
    sleep(2)

    sys.stdout.write('Here are some new codes.\r')
    sys.stdout.flush()
    sleep(2)


if __name__ == '__main__':
    # tt = ProxyPool()
    # tt.main()
    test()
