# -*- coding: UTF-8 -*-
# 请求库
import requests
# 解析库
from bs4 import BeautifulSoup
# 用于解决爬取的数据格式化
import io
import sys


import codecs

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


# 获取微博热搜
def obtainWeiboHotSearch():

    new_headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.40 Safari/537.36 Edg/89.0.774.23"
    }

    # 爬取的网页链接
    r= requests.get("https://s.weibo.com/top/summary?cate=realtimehot/",headers = new_headers)
    # 类型
    # print(type(r))
    print("状态码：" + str(r.status_code))
    # 中文显示
    # r.encoding='utf-8'
    # r.encoding=None
    # print(r.encoding)
    # print("原始数据：")
    # print(r.text)
    result = r.text
    soup = BeautifulSoup(result, "html.parser")
    # 具体标签
    print("格式化输出：")
    #print(soup.prettify())
    #print(soup.title.string)
    ret = []

    url = "https://s.weibo.com/weibo?q="

    # for index in range(10):
    #     strT = "Google",index
    #     ret.append(strT)
    for child in soup.find("tbody"):
        aTag = child.find("a")
        if aTag != -1:
            ret.append({
                "url": str(url + aTag.attrs["href"]),
                "title": aTag.string
            })
    return ret


    # fo = codecs.open("C:\\Users\\zll88\\OneDrive\\syncIP\\ip.txt", "w", "utf-8")
    # fo.write(soup.title.string)
    # fo.close()
