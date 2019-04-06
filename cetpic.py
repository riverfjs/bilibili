import sys
import time
import requests
import threading
from queue import Queue
from lxml import etree

picUrl = Queue()


def getUrl():
    baseUrl = 'http://172.22.80.212'
    url = 'http://172.22.80.212/PHOTO0906CET/'
    res = requests.get(url=url)
    content = etree.HTML(res.text)
    urlList = content.xpath('//pre/a/text()')
    for ii in urlList[1:]:
        newUrl = url + ii
        picUrl.put((newUrl, ii), block=True)


def fetchpic():
    url = picUrl.get(block=True)
    res = requests.get(url=url[0])
    name = "E:\\pic\\cet\\" + url[1]
    with open(name, "wb") as f:
        f.write(res.content)
    print(url[1])


def go():
    threads = []
    while picUrl.empty() is False:
        thread = threading.Thread(target=fetchpic())
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # 同步线程
    print("ok")


def test_one():
    url = ""
    getUrl()
    url = picUrl.get()
    # res = requests.get(url=url)
    # print(re.findall("\.JPG| \.jpg", url))
    print(url)
    # with open(name, "b+") as f:
    #     f.write(res.content)


def main():
    getUrl()
    print("total: ", picUrl.qsize())
    # print(picUrl.empty())
    go()
    # test_one()


if __name__ == '__main__':
    main()

