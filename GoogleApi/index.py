# -*- coding: utf8 -*-

import sys
# 导入环境变量
u='venv'
sys.path.append(u)

import json
# 请求库
import requests
# Google 爬虫库
import GoogleCrawl

def main_handler(event, context):
    _params = event['queryString']
    target = _params['q']
    start = _params['start']
    r = GoogleCrawl.requestGoolgeToJSon(target, start, False)
    # r.text
    result = { 
        "isBase64Encoded":False,
        "statusCode": 200,
         "headers": {"Content-Type":"text/html", "Access-Control-Allow-Origin":"*"},
        "body": r
    }
    return result