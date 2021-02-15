# 爬取真实访问 URL

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
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

# http://www.ijiandao.com/hot/media/douyin/602777c4774c49741e84dca7.html
def obtainRealUrl( destUrl ):
    #destUrl="http://www.ijiandao.com/hot/media/douyin/602777c4774c49741e84dca7.html"
    #destUrl = destUrl.strip().decode(encoding='UTF-8',errors='ignore')
    new_headers = {
       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.40 Safari/537.36 Edg/89.0.774.23"
    }
    r= requests.get(destUrl, headers = new_headers)
    result = r.text
    soup = BeautifulSoup(result, "html.parser")

    t1 = soup.find('div', class_='hot_details_top')
    t2 = t1.find('a')
    # print(t2.attrs["href"])
    return t2.attrs["href"]
