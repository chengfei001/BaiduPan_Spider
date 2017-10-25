#! -*- coding:utf-8 -*-

__author__ = "chengfei"
__Data__ = "20171025"


from requests import  request,utils
from json import loads
import re
from argparse import ArgumentParser


shareurl = ''
filename = ''
Cookie = ''
path = '/'


headers = {
    "Accept": "application/json, text/javascript, text/html, */*; q=0.01",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
        "Referer":"http://pan.baidu.com/disk/home",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Connection": "keep-alive",
    "cookie":Cookie #这里可能有错误#
}

content = r'"app_id":"(\d*)".*"path":"([^"]*)".*"uk":(\d*).*"bdstoken":"(\w*)".*"shareid":(\d*)'  #正则，获取参数值

'''
cookie可以通过登录账号访问百度分享地址后，手动添加资源时用fiddler抓包获取,格式如下：

BAIDUID=C1015A10A3FC569A66923EEF:FG=1; 
BIDUPSID=C1015A10A3FC569A6612AA6EF; 
PSTM=149154382; 
PANWEB=1; 
bdshare_firstime=1497460316; 
BDCLND=vm6Tu2BF8x8%2BwNBLh3XUQD5sfKCUx; 
PSINO=5; 
H_PS_PSSID=22583_22161_1463_2110_17001_21673_22158; 
BDUSS=hqR2RSOVROVmNHREwtV29xVkhBQ3pUb3ZLZlkxM3JGcVFqdmMtY3kzaDlaQUFBJCQAAAAAAAAAAAEAAAA~cQc40NLUy7XEwbm359PwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADJR-FgyUfhYM2; 
STOKEN=69734c07f605e8d0bb09e5513d24497702a32e11029617f54fa3baaa2d9; 
SCRC=0c9e10560d1f5de23b2cf8c42c7484ef; 
Hm_lvt_7a3960b6f0eb0085b7f96ff5e660b0=1492047460,1492396138,1492396201,1492667545; 
Hm_lpvt_7a3960b6f06b0085b7f96ff5e660b0=1492668725; 
PANPSC=1004971751379968%3AWaz2A%2F7j1vWLfEj2viX%2BHu0oj%2BY%2FIsAxoXP3kWK6VuJ5936qezF2bVph1S8bONssvn6mlYdRuXIXUCPSJ19ROAD5r1J1nbMCUL3KDnLECfYjzPb5hCCEJfIbGeUDFmg5zwpdg9WqRKWDBCT3FjnL6jsjP%2FyZiBX26YfN4HZ4D76jyG3uDkPYshZ7OchQK1KQDQpg%2B6XCV%2BSJWX9%2F9F%2FIkt7vMgzc%2BT'
'''


def getBody(url):
    #获取分享页面源码#
    try:
        print("def")
        response = request(method='get', url=url, headers =headers)
        #打印分享页面源码#
        #转换编码为utf-8
        content = response.text.encode('ISO-8859-1').decode('utf-8')
        print(content)


    except Exception as e:
        print("Error:", str(e))



if __name__ == "__main__":
    getBody('http://pan.baidu.com/s/1o8LkaPc')
