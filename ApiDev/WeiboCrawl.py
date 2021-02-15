# -*- coding: UTF-8 -*-
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

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


# 获取微博热搜
def obtainWeiboHotSearch():

    new_headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.47 Safari/537.36 Edg/89.0.774.27"
    }

    # 爬取的网页链接
    r= requests.get("https://s.weibo.com/top/summary?cate=realtimehot/",headers = new_headers)
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
    #print(soup.prettify())
    #print(soup.title.string)
    ret = []

    url = "https://s.weibo.com"

    # for index in range(10):
    #     strT = "Google",index
    #     ret.append(strT)

    for c1 in soup.find("tbody"):
        if (c1==-1 or c1 == None or not isinstance(c1, Tag)):
            continue
        # aTag = c1.find("a")
       # if aTag != -1:
            # ret.append({
            #     "url": str(url + aTag.attrs["href"]),
            #     "title": aTag.string
            # })

        
        # ret.append(str(type(c1)))
        itemData = {
            'url': '',
            'title': '',
            'hotNum': '',
            'tag': '',
            'order': ''
        }
        isAd = False
        # td 集合
        for c2 in c1.children:
            if (c2==-1 or c2 == None or not isinstance(c2, Tag)):
                continue
            if (c2['class'][0] == 'td-01'):
                #print('序号：', c2.string)
                itemData['order'] = c2.string
            elif (c2['class'][0] == 'td-02' and c2.a != None):
                #print('标题：', c2.a.string)
                itemData['title'] = c2.a.string
                #print('链接：', c2.a.attrs["href"])
                itemData['url'] = url + c2.a.attrs["href"]
                if (c2.span != None): 
                    #print('热度：', c2.span.string)
                    itemData['hotNum'] = c2.span.string
            elif (c2['class'][0] == 'td-03' and c2.i != None):
                #print('标签：', c2.i.string)
                itemData['tag'] = c2.i.string
                if (c2.i.string == '荐'):
                    isAd = True
                    
        # 忽略广告
        if (isAd):
            #print("它是广告！")
            continue
            
        #填充返回值
        ret.append(itemData)
    
        #print()    


    return ret


    # fo = codecs.open("C:\\Users\\zll88\\OneDrive\\syncIP\\ip.txt", "w", "utf-8")
    # fo.write(soup.title.string)
    # fo.close()
