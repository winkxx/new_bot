from flask import Flask,request
from requests import get,post

import os

status =""
app = Flask(__name__)
SITE_NAME = 'http://127.0.0.1:8080/'

@app.route('/jsonrpc',methods=['POST'])
def proxypost():
    path="jsonrpc"
    #print("post")
    #print(f'{SITE_NAME}{path}')
    url=f'{SITE_NAME}{path}?'
    #print(request.form)
    student = request.data
    #print(student)
    #获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定
    return (post(url=url,data=student).content)



@app.route('/jsonrpc/',methods=['GET'])
def proxyget():
    path="jsonrpc"
    #print(f'{SITE_NAME}{path}')
    url=f'{SITE_NAME}{path}?'
    #print(request.args)
    par=request.args
    #http://127.0.0.1:5000/jsonrpc?jsonrpc=2.0&method=aria2.getGlobalStat&id=QXJpYU5nXzE2MTM4ODAwNTBfMC44NTY2NjkzOTUyMjEzNDg3&params=WyJ0b2tlbjp3Y3k5ODE1MSJd&
    return get(url=url,params=par).content


if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
