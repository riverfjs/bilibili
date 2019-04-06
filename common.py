import re
import json
import requests

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',  # noqa
}


def get_content(url, headers):
    res = requests.get(url=url, headers=headers)

class Base(object):
    def __init__(self, *args):
        self.stream = {}
        self.cookie = ''

if __name__ == '__main__':
    print(type(fake_headers))