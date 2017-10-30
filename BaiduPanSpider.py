#! -*- coding:utf-8 -*-


'''
操作百度网盘，自动添加资源到网盘。
注意点：
爬取源码可以使用Requests模块
* 获取cookie（可以手动登录然后抓包获取）
* 首先爬取如：http://pan.baidu.com/s/1bp0csmN，获取源码
* 解析源码，筛选出该页面分享资源的名称、shareid、from（uk)、bdstoken、appid（app_id）。
* 构造post包（用来添加资源到网盘），该包需要用到以上4个参数，当然还有一个最重要的就是cookie
在post包的url中还有一个logid参数，内容可以随便写，应该是个随机值然后做了base64加密。
在post包的payload中，filelist是资源名称，格式filelist=["/name.mp4"]，path为保存到那个目录下，格式path=/pathname
'''

__author__ = "chengfei"
__Data__ = "20171025"

from requests import  request,utils,post
from json import loads
import re
from argparse import ArgumentParser
import logging

'''
小瓶子抓取的数据包
https://pan.baidu.com/share/transfer?shareid=290489260&from=3527831162&ondup=newcopy&async=1&bdstoken=85635ac68ceac87648418fa009243185&channel=chunlei&clienttype=0&web=1&app_id=250528&logid=MTUwOTM0NzA4MDA5MjAuMzc5MjgwNzI0ODg3Mzc5Mg==
filelist:["/新建文件夹(7)/姥姥语录-倪萍"]
path:/
'''


res_content = r'"app_id":"(\d*)".*"path":"([^"]*)".*"uk":(\d*).*"bdstoken":"(\w*)".*"shareid":(\d*)'  # 正则，获取参数值
shareurl = ''
filename = ''
Cookie = ''
path = '/'


class baiduPanSpider:
    def __init__(self):
        self.parameter = re.compile(res_content)

        # self.shareurl = ''
        # self.filename = ''
        # self.Cookie = ''
        self.path = '/'
        self.app_id = ""
        self.uk = ""
        self.bdstoken = ""
        self.shareid = ""
        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Accept': 'Accept=application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'Accept-Language=zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest',
            'Referer': 'https://pan.baidu.com/s/1bp0csmN',
            'Cookie':'BAIDUID=D32E0E6A74B4E4C441C9F738F621367F:FG=1; PANWEB=1; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1509008858,1509347006,1509347062; cflag=15%3A3; FP_UID=49f66836d766350e8883279c0479925a; BDUSS=9Dd0p1aFo2b0N0UkRxUEszUFJrckNuVENYc3R6SWFmTXkyZGJ1eHRJNU5OQmxhSVFBQUFBJCQAAAAAAAAAAAEAAACZxAMAY2hlbmdmZWkwMDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE2n8VlNp~FZMG; STOKEN=f462ded76da2ea1e9bf4a766b686670cd65740b84d7f41b6ec088751f8bc19f1; SCRC=a8095d2ab2d97437660899ad204b5a9c; PANPSC=16055253465164159052%3A9qIJoSpryQ%2Fb41ZnUGXO%2BMxDaFs%2FKMrufnkgCRPBFD%2Bqv5jBm4hVt4M6La9EbgvRSav%2FOZ6AnJ0YKZNubvMnxOckY2sOTxob9i4CW8ceHnrqPo4uQmxPcVfUDd9arCIiYTASXnFzAgG1T%2BAf1Zi%2BmWNtiaXV6jA2rsgnNL%2BLYct9tn9thbnTpv7IiW4JizVanZlv3sbf6BI%3D; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1509347062',
            'Connection': 'keep-alive'
            }

    def run(self,url):


    def getSourcePage(self,url):
        #获取资源页面#
        try:
            response = request(method='get', url=url, headers=self.headers)

            # 打印分享页面源码#
            # 转换编码为utf-8
            content = response.text.encode('ISO-8859-1').decode('utf-8')

            parameterValue = self.parameter.findall(content)
            app_id = parameterValue[0][0]
            path = parameterValue[0][1]
            uk = parameterValue[0][2]
            bdstoken = parameterValue[0][3]
            shareid = parameterValue[0][4]
        except Exception as e:
            print("Error:", str(e))

    def addToMyDisk(self):
        url_post = "https://pan.baidu.com/share/transfer?shareid=" + self.shareid + "&from=" + self.uk + "&ondup=newcopy&async=1&bdstoken=" + self.bdstoken + "&channel=chunlei&clienttype=0&web=1&app_id=" + self.app_id + "&logid=MTUwOTM0NzA4MDA5MjAuMzc5MjgwNzI0ODg3Mzc5Mg=="
        payload = "filelist=%5B%22" + path + "%22%5D&path=/mobi/"  # 资源名称与要保存的路径
        # print("[Info]Url_Post:", url_post)
        # print("[Info]payload:", payload)

        try:
            # post post post 「get」折腾我了一周#
            response = post(url=url_post, headers=self.headers, data=payload)
            result = loads(response.text)
            tag = result["errno"]
            if tag == 0:
                print(result + "Add Success")
            else:
                print(result + "Have Error")
        except Exception as e:
            print("Error:", str(e))


def main():
    global  Cookie,path,shareurl,filename



if __name__ == "__main__":
    main()
    spider = baiduPanSpider()

    try:
        with open(filename, "r") as urlsFile:
            urls = [i.strip("\n").strip("\r") for i in urlsFile.readline()]
        for url in urls:
            logging.info("shareurl:" + url)
            spider.run(url)
    except IOError:
            logging.error("Error:filename error)"

