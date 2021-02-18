
import sys
# 导入环境变量
u='venv'
sys.path.append(u)

import WeiboCrawl
import RealUrlCrawl
import IjiandaoCrawl
import time
import json

def main_handler(event, context):
    #res = WeiboCrawl.obtainWeiboHotSearch()
    # res = {
    #     'path': event['path'],
    #     'params': event['queryString'],
    #     '是否存在参数：': 'type' in event['queryString'].keys()
    # }
    print("params：", 'type' in event['queryString'].keys())
    _return_dict= {'code': -1, 'msg': '处理失败',  "expired_time": -1, 'time_stamp': -1, 'type': 'weibo', 'result': False}

    _path = event['path']
    _params = event['queryString']

    if _path == '/hotSearch/obtainRealUrl':
        _return_dict = obtainRealUrl(_params)
    elif _path == '/hotSearch/list':
        _return_dict = hotSearch(_params)
    else: # '/hotSearch'
        _return_dict = hotSearch(_params)

    result = {
        "isBase64Encoded":False,
        "statusCode": 200,
        "headers": {"Content-Type":"text/html"},
        "body": json.dumps(_return_dict)
    }
    return result

# 热搜
def hotSearch( params ):
    return_dict= {'code': -1, 'msg': '处理失败',  "expired_time": -1, 'time_stamp': -1, 'type': 'weibo', 'result': False}
    if 'type' not in params :
        return_dict['msg'] = "未传类型参数"
        return return_dict
    type = params['type']
    return_dict['type'] = type
    if type == "weibo":
        result = WeiboCrawl.obtainWeiboHotSearch()
    else:
        result = IjiandaoCrawl.obtainHotSearch(type)
    if len(result) > 0:
        if (type == "weibo"):#剔除置顶的这一条
            result.pop(0)
        return_dict['result']=result
        return_dict['code']=0
        return_dict['msg']='处理成功'
    else:
        return_dict['msg']="微博爬取失败！"

    # 过期时间，用于做客户端缓存 毫秒单位, 目前过期时间为 10s
    return_dict['expired_time'] = (time.time() + 10) * 1000
    return_dict['time_stamp'] = time.time() * 1000

    return return_dict

# 真实 Url 获取
def obtainRealUrl( params ):
    return_dict= {'code': -1, 'msg': '处理失败',  "expired_time": -1, 'time_stamp': -1, 'type': 'weibo', 'result': False}
    if 'destUrl' not in params :
        return_dict['msg'] = "未传指定Url"
        return return_dict
    destUrl=params.get('destUrl')

    if (destUrl == None or destUrl == ''):
        return_dict['code']=-1
        return_dict['msg']="destUrl 为空"
    else:
        try:
            return_dict['test'] = destUrl
            return_dict['url'] = RealUrlCrawl.obtainRealUrl(destUrl)
            return_dict['code']=0
            return_dict['msg']='处理成功'
        except:
            return_dict['msg']="爬取发生异常"
    return return_dict