# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import sys
import re
import json
import csv
import time


def get_xxxx(lis):
    for v in lis:
        content = v.next
        if content.__contains__("xxxxx"):
            t = content.split("=")[1].strip().strip(";")
            js = json.loads(t)
            return js
    return None


def write_csv(path, data_row):
    with open(path, 'a+') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)


def read_proxy(path):
    with open(path, "r", encoding="utf-8") as r:
        file = r.read().split("\n")
        file = [[j for j in v.split(" ") if not "".__eq__(j)] for v in file]
        proxy = [v[1] + ":" + v[2] for v in file]
        ht = [v[5] for v in file]
        return dict(zip(ht, proxy))


if __name__ == '__main__':
    url = "https://hz.lianjia.com/fangjia"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        "Vary": "Accept-Encoding"
    }
    path = "F:\workspace\scraping\data"
    proxys = read_proxy("F:\workspace\scraping\data\\proxy")
    print(sys.getdefaultencoding())
    s = requests.session()
    s.keep_alive = False
    s.proxis = proxys
    s.headers = headers
    r = s.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html')
    print(soup.title.string)
    script_tags = soup.find_all("script")
    xxxx = get_xxxx(script_tags)

    regionInfoList = xxxx['regionInfo']['district']
    for v in regionInfoList:
        quanpin_url = v['quanpin_url']
        url1 = url + "/" + quanpin_url
        path1 = path + "/region.csv"
        print(url1)
        # with open(path1, "w") as f:
        #     csv_write = csv.writer(f)
        #     csv_head = ["date", "region", "online_house_num", "monthTrans", "day90Sold", "sold_house_num",
        #                 "houseAmount",
        #                 "customerAmount", "showAmount"]
        #     csv_write.writerow(csv_head)

        r = s.get(url1)
        if r.status_code != 200:
            print("get error %s".format(url1))
            time.sleep(15)
            r = requests.get(url1)
            continue
        soup = BeautifulSoup(r.text, 'html')
        script_tags = soup.find_all("script")
        xxxx = get_xxxx(script_tags)

        online_house_num = xxxx['sellList']['count']
        print("online_house_num:", online_house_num)
        sold_house_num = xxxx['soldList']['count']
        print("sold_house_num:", sold_house_num)

        day90Sold = xxxx['day90Sold']
        print("day90Sold:", day90Sold)
        monthTrans = xxxx['bdaData']['monthTrans']
        print("monthTrans:", monthTrans)

        houseAmount = xxxx['bdaData']['houseAmount']
        print("houseAmount:", houseAmount)
        customerAmount = xxxx['bdaData']['customerAmount']
        print("customerAmount:", customerAmount)

        showAmount = xxxx['bdaData']['showAmount']
        print("showAmount:", showAmount)

        date = xxxx['timeFactor']['update'].split("T")[0]
        print("date", date)
        write_csv(path1,
                  [date, quanpin_url, online_house_num, monthTrans, day90Sold, sold_house_num, houseAmount,
                   customerAmount,
                   showAmount])
