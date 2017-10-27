#! -*- coding:utf-8 -*-

__author__ = "chengfei"
__Data__ = "20171025"


from requests import  request,utils
from json import loads
import re
from argparse import ArgumentParser
import logging


shareurl = ''
filename = ''
Cookie = 'BAIDUID=D32E0E6A74B4E4C441C9F738F621367F:FG=1; PANWEB=1; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1509008858; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1509082730; cflag=15%3A3; FP_UID=49f66836d766350e8883279c0479925a; BDUSS=9Dd0p1aFo2b0N0UkRxUEszUFJrckNuVENYc3R6SWFmTXkyZGJ1eHRJNU5OQmxhSVFBQUFBJCQAAAAAAAAAAAEAAACZxAMAY2hlbmdmZWkwMDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE2n8VlNp~FZMG; STOKEN=f462ded76da2ea1e9bf4a766b686670cd65740b84d7f41b6ec088751f8bc19f1; SCRC=a8095d2ab2d97437660899ad204b5a9c; PANPSC=2417222962666375702%3A9qIJoSpryQ%2Fb41ZnUGXO%2BMxDaFs%2FKMrufnkgCRPBFD%2Bqv5jBm4hVt4M6La9EbgvREwmAcbtoLMCQxqFK7Vw7LOckY2sOTxob9i4CW8ceHnrqPo4uQmxPcVfUDd9arCIiYTASXnFzAgG1T%2BAf1Zi%2BmWNtiaXV6jA2rsgnNL%2BLYct9tn9thbnTpv7IiW4JizVanZlv3sbf6BI%3D'
path = '/'
'''
'Accept': '*/*',
'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
cookie可以通过登录账号访问百度分享地址后，手动添加资源时用fiddler抓包获取,格式如下：
'Cookie':'BAIDUID=D32E0E6A74B4E4C441C9F738F621367F:FG=1; PANWEB=1; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1509008858; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1509082730; cflag=15%3A3; FP_UID=49f66836d766350e8883279c0479925a; BDUSS=9Dd0p1aFo2b0N0UkRxUEszUFJrckNuVENYc3R6SWFmTXkyZGJ1eHRJNU5OQmxhSVFBQUFBJCQAAAAAAAAAAAEAAACZxAMAY2hlbmdmZWkwMDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE2n8VlNp~FZMG; STOKEN=f462ded76da2ea1e9bf4a766b686670cd65740b84d7f41b6ec088751f8bc19f1; SCRC=a8095d2ab2d97437660899ad204b5a9c; PANPSC=2417222962666375702%3A9qIJoSpryQ%2Fb41ZnUGXO%2BMxDaFs%2FKMrufnkgCRPBFD%2Bqv5jBm4hVt4M6La9EbgvREwmAcbtoLMCQxqFK7Vw7LOckY2sOTxob9i4CW8ceHnrqPo4uQmxPcVfUDd9arCIiYTASXnFzAgG1T%2BAf1Zi%2BmWNtiaXV6jA2rsgnNL%2BLYct9tn9thbnTpv7IiW4JizVanZlv3sbf6BI%3D',
'Host': 'pan.baidu.com',
'Pragma': 'no-cache',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
'''
'''
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


headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    #能用的
    #'Cookie':'PANPSC=12067747241709542613%3anZglRs3jFmhgG2mKJdpk0yOAoXNFwReXE%2fUU18L%2fNaPGlNjpEQf069wksVDpO%2beIP2GfA841LsJ89vQkxk9MjDpmkI78m9qy2bVdhq2QaMJE%2bhLVkDMtishTKu%2bdwTb%2fGdoA%2fVzJUP%2bQqfggdE%2f8ljAuFRSmSxRJzENoWz8oyu5%2beSAJE8EUP0rlgxafUjiqHOxPxwQDn7UrkMqRkNV6mA%3d%3d; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1509088324; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1508827939,1508828244,1508996945,1509009120; BDCLND=M1AyeUfA9zLjdkUSMBrNG0HY5i%2Bdp82VXRDqMU5XPZk%3D; SCRC=f05329f6a3d2c55d0444f91923a42345; STOKEN=c3ba05c59af435242ee418337eb0427cf97d4469a2950ca5a17f08731d2a76a9; PANWEB=1; bdshare_firstime=1462952408001; cflag=15%3A3; H_PS_PSSID=1461_21119_17001_22158; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; PSINO=1; FP_UID=0b91dad8b2c877f1ad86ffca297bd047; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDRCVFR[d9MwMhSWl4T]=mk3SLVN4HKm; H_WISE_SIDS=119429_102572_100806_114178_100098_114244_119309_119024_118887_118863_118857_118826_118787_118146_107312_119045_118969_119884_117585_117331_117244_119771_117431_118996_119596_119285_119931_115535_118966_117553_119499_119945_117934_119143_119528_119320_116407_119209_110085_119732_119403; BDSFRCVID=QCCsJeC62C1jevjZgb06-VPE2HuNpfnTH6aodqk0F1q1beWO8imYEG0PqM8g0KubQ2zmogKK0mOTHUvP; H_BDCLCKID_SF=tJPeoCKMtD03HnRY-P4_bnDtbhbt2430-57-3-bO-jrjDnCrDUbUKUI8LNDHXtc-K672hqTqK-IVSxJHD4_byP0N-nO7ttoyBe_L_nOM5R0V8CD43tT-5ML1Db3DhTvMtg3t3JnTB45oepvoD-cc3MkBXn0EJj0JfRCJ_CtQb-3bK4c9D5Lbq4C85aReLM3eWDTm_Dos3IJpMMbLbURJQDuZ0-_HK4KeBD7Z-pPKKR7pof5PbUuMhJLBhfbEBxc03mkjbpbDfn02OP5PXj0K-44syP4j2xRnWNTqbIF-tDLaMItGDTRb5nbH-fcKhtRXHD7XVMjn0-Okeq8CDx-aM4LBMR6M5j8qHGcTKCodblr2eRr2y5jHhP0LMN3lJR_DKDTU2KnVaxTpsIJMKfFWbT8U5f5IJJTLaKviaKJEBMb1StQMe4bK-TrLea-8tUK; BDUSS=FjQkhQa3cyem1NZ2lGMXpaLVNvVTIwVEJKWGlUfndkT1UtYkloNDRocEFxSk5aSVFBQUFBJCQAAAAAAAAAAAEAAACZxAMAY2hlbmdmZWkwMDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAbbFlAG2xZa3; __cfduid=d3b595675045b8a1a372c0abfbee2bd681494899684; BAIDUCUID=++; BAIDUID=046F90325A6D2F252B3D9F5281BEBE93:FG=1; BIDUPSID=046F90325A6D2F252B3D9F5281BEBE93; PSTM=1462613342',
    #能用的
    'Cookie':'PANPSC=14046934356659016807%3A9qIJoSpryQ%2Fb41ZnUGXO%2BMxDaFs%2FKMrufnkgCRPBFD%2Bqv5jBm4hVt4M6La9EbgvRcd2wy6RYk5pvi%2FiP55OazeckY2sOTxob9i4CW8ceHnrqPo4uQmxPcVfUDd9arCIiYTASXnFzAgG1T%2BAf1Zi%2BmWNtiaXV6jA2rsgnNL%2BLYct9tn9thbnTpv7IiW4JizVanZlv3sbf6BI%3D; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1509088324; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1508827939,1508828244,1508996945,1509009120; BDCLND=M1AyeUfA9zLjdkUSMBrNG0HY5i%2Bdp82VXRDqMU5XPZk%3D; SCRC=f05329f6a3d2c55d0444f91923a42345; STOKEN=c3ba05c59af435242ee418337eb0427cf97d4469a2950ca5a17f08731d2a76a9; PANWEB=1; bdshare_firstime=1462952408001; cflag=15%3A3; H_PS_PSSID=1461_21119_17001_22158; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; PSINO=1; FP_UID=0b91dad8b2c877f1ad86ffca297bd047; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDRCVFR[d9MwMhSWl4T]=mk3SLVN4HKm; H_WISE_SIDS=119429_102572_100806_114178_100098_114244_119309_119024_118887_118863_118857_118826_118787_118146_107312_119045_118969_119884_117585_117331_117244_119771_117431_118996_119596_119285_119931_115535_118966_117553_119499_119945_117934_119143_119528_119320_116407_119209_110085_119732_119403; BDSFRCVID=QCCsJeC62C1jevjZgb06-VPE2HuNpfnTH6aodqk0F1q1beWO8imYEG0PqM8g0KubQ2zmogKK0mOTHUvP; H_BDCLCKID_SF=tJPeoCKMtD03HnRY-P4_bnDtbhbt2430-57-3-bO-jrjDnCrDUbUKUI8LNDHXtc-K672hqTqK-IVSxJHD4_byP0N-nO7ttoyBe_L_nOM5R0V8CD43tT-5ML1Db3DhTvMtg3t3JnTB45oepvoD-cc3MkBXn0EJj0JfRCJ_CtQb-3bK4c9D5Lbq4C85aReLM3eWDTm_Dos3IJpMMbLbURJQDuZ0-_HK4KeBD7Z-pPKKR7pof5PbUuMhJLBhfbEBxc03mkjbpbDfn02OP5PXj0K-44syP4j2xRnWNTqbIF-tDLaMItGDTRb5nbH-fcKhtRXHD7XVMjn0-Okeq8CDx-aM4LBMR6M5j8qHGcTKCodblr2eRr2y5jHhP0LMN3lJR_DKDTU2KnVaxTpsIJMKfFWbT8U5f5IJJTLaKviaKJEBMb1StQMe4bK-TrLea-8tUK; BDUSS=FjQkhQa3cyem1NZ2lGMXpaLVNvVTIwVEJKWGlUfndkT1UtYkloNDRocEFxSk5aSVFBQUFBJCQAAAAAAAAAAAEAAACZxAMAY2hlbmdmZWkwMDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAbbFlAG2xZa3; __cfduid=d3b595675045b8a1a372c0abfbee2bd681494899684; BAIDUCUID=++; BAIDUID=046F90325A6D2F252B3D9F5281BEBE93:FG=1; BIDUPSID=046F90325A6D2F252B3D9F5281BEBE93; PSTM=1462613342',
    'Host': 'pan.baidu.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
res_content = r'"app_id":"(\d*)".*"path":"([^"]*)".*"uk":(\d*).*"bdstoken":"(\w*)".*"shareid":(\d*)'  #正则，获取参数值




def getBody(url):
    #获取分享页面源码#
    try:
        # logging.warning(headers)

        response = request(method='get', url=url, headers =headers)
        # html = response.text.strip()
        # if html == "":
        #     logging.error('无输出')
        # else:
        #     logging.warning(html)
        #     logging.warning(html)

        #打印分享页面源码#
        #转换编码为utf-8
        content = response.text.encode('ISO-8859-1').decode('utf-8')

        #使用正则表达式有关资源的参数app_id,path,uk,bdstoken,shareid
        # content = r'"app_id":"(\d*)".*"path":"([^"]*)".*"uk":(\d*).*"bdstoken":"(\w*)".*"shareid":(\d*)'  # 正则，获取参数值
        res_content = r'"app_id":"(\d*)".*"path":"([^"]*)".*"uk":(\d*).*"bdstoken":"(\w*)".*"shareid":(\d*)'  # 正则，获取参数值
        p = re.compile(res_content)
        L = p.findall(content)
        # logging.warning(L)#
        app_id = L[0][0]
        path = L[0][1]
        uk = L[0][2]
        bdstoken = L[0][3]
        shareid = L[0][4]
        url_post = "https://pan.baidu.com/share/transfer?shareid=" + shareid + "&from=" + uk + "&bdstoken=" + bdstoken + "&channel=chunlei&clienttype=0&web=1&app_id=" + app_id + "&logid=MTUwOTA4ODUyNjUxNDAuMDYyMDEzMDYxMTc3MDE2MzI2"
        payload = "filelist=%5B%22" + path + "%22%5D&path=/"  # 资源名称与要保存的路径
        print("[Info]Url_Post:", url_post)
        print("[Info]payload:", payload)
        response = request(method='get', url=url_post, headers=headers)
        logging.warning(response.text)
        result = loads(response.text)
        tag = result["errno"]
        print
        tag
        if tag == 0:
            print
            "[Result]Add Success"
        elif tag == 12:
            print
            "[Result]Already Exist"
        else:
            print
            "[Result]Have Error"
    except Exception as e:
        print("Error:", str(e))



if __name__ == "__main__":
    getBody('https://pan.baidu.com/s/1bp0csmN')
