from flask import Flask, request

import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '开始搞起12'

@app.route('/hotSearch',methods=["GET"])
def hotSearch():
    # 默认返回内容
    return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
    
    # 获取传入的params参数
    get_data=request.args.to_dict()
    index=get_data.get('index')
    return_dict['result']=index
    return json.dumps(return_dict, ensure_ascii=False)

if __name__ == '__main__':
    # 不用每次重新启动
    app.debug = True
    app.run(host='0.0.0.0')