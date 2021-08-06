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
import json

# import codecs

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
def requestGoolge(target, debug): 
    new_headers = {
       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.40 Safari/537.36 Edg/89.0.774.23"
    }
    htmlRes = ""
    if debug:
        f = open("google_search.html")
        htmlRes = f.read(-1)
        f.close()
    else:
        # hl 界面语言 
        r = requests.get("https://www.google.com.hk/search?hl=zh-CN&q=" + target, headers = new_headers)
        htmlRes = r.text

    soup = BeautifulSoup(htmlRes, "html.parser")
    # 找到搜索结果
    result = str(soup.select('#search')).lstrip('[').rstrip(']')
    # 写入测试文件
    if debug:
        f = open("out.html", mode='w')
        f.write(str(result))
        f.close()
    # 使用 soup 提取 search
    return result

# 以 JSON 格式吐出数据
def requestGoolgeToJSon(target, startIndex, debug): 
    new_headers = {
       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.40 Safari/537.36 Edg/89.0.774.23"
    }
    htmlRes = ""
    if debug:
        f = open("google_search.html")
        htmlRes = f.read(-1)
        f.close()
    else:
        # hl 界面语言 
        # r = requests.get("https://www.google.com.hk/search?hl=zh-CN&q=" + target + "&start=" + startIndex, headers = new_headers)
        r = requests.get("https://www.google.com.hk/search?hl=zh-CN&q=" + target + "&start=" + startIndex, headers = new_headers)
        htmlRes = r.text

    soup = BeautifulSoup(htmlRes, "html.parser")
    result = {}
    # 查找搜索耗时
    try:
        time = soup.find('div', id='result-stats').nobr.string.lstrip().lstrip('（').rstrip().rstrip('）')
        result['time_consuming'] = time
    except:
        print("time 解析失败")
    
    # print(soup.find('div', id = 'rso'))
    list = []
    result['list'] = list

    # 查询所有搜索结果
    for s in soup.find_all('div', class_='tF2Cxc'):
        s1 = s.find('div', class_='yuRUbf')
        s2 = s.find('div', class_='IsZvec')
        
        try:
            d = s2.div.stripped_strings
            description = ""
            showTime = ""

            for dd in d:
                s = str(dd.strip().replace("\n", "").replace("  ", ""))
                description += s
            
            itemData = {
                'title': s1.a.h3.string.strip(),
                'url': s1.a['href'],
                'description': description,
                'showTime': showTime
            }
            list.append(itemData)
        except:
            print("reslut 解析失败")    
    # 找到搜索结果
    # result = str(soup.select('#search')).lstrip('[').rstrip(']')
    # 写入测试文件
    # if debug:
    #     f = open("out.html", mode='w')
    #     f.write(str(result))
    #     f.close()
    # 使用 soup 提取 search
    return json.dumps(result)