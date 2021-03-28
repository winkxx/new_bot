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

@app.route('/', methods=['GET'])
def index():
    text = '''
    唤醒成功！！！(也许)
    
    ********** pixiv相关 **********
/pixivuser - 打包下载P站画师的全部作品上传至云盘
/pixivusertg - 压缩打包下载P站画师的全部作品发送到TG
/pixivuserphoto - 下载P站画师的全部作品图片方式发送
pixivusertele - 下载P站画师的全部作品网页方式发送
在命令后加入作品ID，使用示例
/pixivuser 9675329

/pixivpid - 发送pixiv该id的图片
在命令后加入作品ID，使用示例
/pixivpid 88339301

********** aria2相关 **********
/magfile - 推送种子文件至aria2下载
/mirror - 推送直链至aria2下载上传至网盘
/mirrortg - 推送直链至aria2下载发送到TG
/magnet - 推送磁力链接至aria2下载
以上在命令后加入链接

********** 其它相关 **********
/downtgfile - 发送TG文件并上传至网盘
发送 /downtgfile 后按提示发送文件即可

/search - 在哔咔搜索本子
示例 /search 本子名

/rclonecopyurl - 用rclonecopyurl的方式直接上传直链文件
示例 /rclonecopyurl 文件直链

/getfileid - 发送文件获取fileid
发送 /getfileid  后按提示发送文件即可

/getfile - 发送fileid来获取文件
示例 /getfile  文件直链

/video - 使用youtube-dl下载视频
示例 /getfile  视频链接
目前测试youtube和哔哩哔哩(不包括番剧)完美适配

Bot相关联系：https://t.me/Ben_chao'''
    return text, 200

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
