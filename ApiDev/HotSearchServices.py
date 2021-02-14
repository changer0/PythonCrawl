from flask import Flask, request

import json

import weiboCrawl

import time

app = Flask(__name__)

@app.route('/hotSearch',methods=["GET"])
def hotSearch():
    # 默认返回内容
    return_dict= {'code': 200, 'msg': '处理成功',  "expired_time": -1, 'time_stamp': -1, 'result': False}
    
    # 获取传入的params参数
    get_data=request.args.to_dict()
    index=get_data.get('index')

    result = weiboCrawl.obtainWeiboHotSearch()
    if len(result) > 0:
        result.pop(0)
        return_dict['result']=result
    else:
        return_dict['msg']="微博爬取失败！"
        return_dict['code']=-1
    # 过期时间，用于做客户端缓存 毫秒单位, 目前过期时间为 10s
    return_dict['expired_time'] = (time.time() + 10) * 1000
    return_dict['time_stamp'] = time.time() * 1000
    
    return json.dumps(return_dict, ensure_ascii=False)

if __name__ == '__main__':
    # 不用每次重新启动
    app.debug = True
    app.run(host='0.0.0.0')