# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import sys

if __name__ == '__main__':
    url = "https://hz.lianjia.com/fangjia"
    file = open("/data/home.html", "w", encoding='utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        "Vary": "Accept-Encoding"
    }

    print(sys.getdefaultencoding())
    r = requests.get(url, headers)
    print(r.encoding)
    print(r.status_code)

    file.write("r.status_code\n")
    file.write(str(r.status_code))
    file.write("\n")
    file.write("r.text\n")
    file.write(r.text)
    file.write("\n")
    file.write("r.json()\n")
    file.write("\n")
