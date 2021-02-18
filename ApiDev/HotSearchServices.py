from flask import Flask, request

import json

import WeiboCrawl
import RealUrlCrawl
import IjiandaoCrawl
import time

app = Flask(__name__)

@app.route('/hotSearch/list',methods=["GET"])
def hotSearch():
    # 默认返回内容
    return_dict= {'code': 200, 'msg': '处理成功',  "expired_time": -1, 'time_stamp': -1, 'type': 'weibo', 'result': False}

    # 获取传入的params参数
    get_data=request.args.to_dict()
    type=get_data.get('type') # weibo douyin

    if type == None or type == '':
        type = 'weibo'

    return_dict['type'] = type

    if type == "weibo":
        result = WeiboCrawl.obtainWeiboHotSearch()
    else:
        result = IjiandaoCrawl.obtainHotSearch(type)


    if len(result) > 0:
        if (type == "weibo"):
            result.pop(0)
        return_dict['result']=result
    else:
        return_dict['msg']="微博爬取失败！"
        return_dict['code']=-1

    # 过期时间，用于做客户端缓存 毫秒单位, 目前过期时间为 60s
    return_dict['expired_time'] = (time.time() + 60) * 1000
    return_dict['time_stamp'] = time.time() * 1000
    
    return json.dumps(return_dict, ensure_ascii=False)

@app.route('/hotSearch/obtainRealUrl',methods=["GET"])
def obtainRealUrl():
    # 获取传入的params参数
    get_data=request.args.to_dict()
    destUrl=get_data.get('destUrl')
    # 默认返回内容
    return_dict= {'code': 200, 'msg': '处理成功',  'url': '', 'test':''}
    if (destUrl == None or destUrl == ''):
        return_dict['code']=-1
        return_dict['msg']="destUrl 为空"
    else:
        try:
            return_dict['test'] = destUrl
            return_dict['url'] = RealUrlCrawl.obtainRealUrl(destUrl)
        except:
            return_dict['msg']="爬取发生异常"


    return json.dumps(return_dict, ensure_ascii=False)

if __name__ == '__main__':
    # 不用每次重新启动
    app.debug = True
    app.run(host='0.0.0.0')