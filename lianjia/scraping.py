# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import sys
import re
import json
import csv


def get_moon_aver_price(lis):
    i = 0
    while i < len(lis):
        content = lis[i].text
        if content.__contains__("链家参考均价"):
            break
        i += 1
    price = int(lis[i + 1].text)
    return price


def get_online_house_num(lis):
    result = 0
    for v in lis:
        content = v.text
        if content.__contains__("在售房源"):
            result = re.findall(r"\d+\.?\d*", content)[0]
    return result


def get_sold_in_90d(lis):
    result = 0
    for v in lis:
        content = v.text
        if content.__contains__("最近90天内成交房源"):
            result = re.findall(r"\d+\.?\d*", content)[1]
    return result


def get_xxxx(lis):
    for v in lis:
        content = v.next
        if content.__contains__("xxxxx"):
            t = content.split("=")[1].strip().strip(";")
            js = json.loads(t)
            return js
    return None


def print_x(x):
    print("%s".format(x), x)


def write_csv(path, data_row):
    with open(path, 'a+') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)


if __name__ == '__main__':
    url = "https://hz.lianjia.com/fangjia"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        "Vary": "Accept-Encoding"
    }

    path = "/mnt/f/workspace/scraping/data/hangzhou.csv"

    # with open(path, "w") as f:
    #     csv_write = csv.writer(f)
    #     csv_head = ["date", "online_house_num", "monthTrans", "day90Sold", "sold_house_num", "houseAmount",
    #                 "customerAmount", "showAmount"]
    #     csv_write.writerow(csv_head)

    print(sys.getdefaultencoding())
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.text, 'html')
    print()
    print(soup.title.string)
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
    write_csv(path,
              [date, online_house_num, monthTrans, day90Sold, sold_house_num, houseAmount, customerAmount, showAmount])


