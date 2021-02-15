# http://www.ijiandao.com/hot/complex
# 请求库
import requests
# 解析库
from bs4 import BeautifulSoup
# 用于解决爬取的数据格式化
import io
import sys
from bs4 import NavigableString
from bs4 import Tag
import codecs



# 获取微博热搜
def obtainHotSearch():

    new_headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.47 Safari/537.36 Edg/89.0.774.27"
    }

    # 爬取的网页链接
    r= requests.get("http://www.ijiandao.com/hot/media/douyin",headers = new_headers)
    # 类型
    # print(type(r))
    # print("状态码：")
    # print(r.status_code)
    # 中文显示
    # r.encoding='utf-8'
    # r.encoding=None
    # print(r.encoding)
    # print("原始数据：")
    # print(r.text)
    result = r.text
    soup = BeautifulSoup(result, "html.parser")
    # 具体标签
    #print("格式化输出：")
    # print(soup.prettify())
    #print(soup.title.string)
    ret = []

    url = "http://www.ijiandao.com"

    for c1 in soup.find('ul', class_='hot_new_list hot_classify'):
        if (c1==-1 or c1 == None or not isinstance(c1, Tag)):
            continue


        itemData = {
            'url': '',
            'title': '',
            'hotNum': '',
            'tag': '',
            'order': ''
        }
        isAd = False
        c2Index = 0
        # td 集合
        for c2 in c1.children:
            if (c2==-1 or c2 == None or not isinstance(c2, Tag)):
                continue

            if c2Index == 0:
                #序号
                #print("序号：", c2.string)
                itemData['order'] = c2.string
            elif c2Index == 1:
                #url 标题
                #print("标题：", c2.a.string)
                itemData['title'] = c2.a.string
                itemData['url'] = url + c2.a.attrs["href"]
            elif c2Index == 2:
                #热度
                #print("标题：", c2.string)
                itemData['hotNum'] = c2.string
            c2Index = c2Index + 1
                    
        # 忽略广告
        if (isAd):
            #print("它是广告！")
            continue
            
        #填充返回值
        ret.append(itemData)

    return ret