# -*- coding: utf-8 -*-
import os

import requests

import config
from Proxy.IPPool import getIP
from config import COOKIE_DICT,TARGET
from crawler.APIdatadump import datadump
from crawler.crawler.API import getAPIdata
from crawler.crawler.index import getindex
from error.error import GetIndexError, BanIPError, APIError


indexlist = []
APIProxy = None
TatgetTag = False

def indexgeter(qi):
    TatgetTag = False
    indexlist = []
    # 从日志中读取上次进行到的位置
    lastpage, lastgid, lasttoken = getlastindex()
    lastpage = int(lastpage)
    print('为API爬虫获取代理')
    APIProxy = getIP()
    # 借用API的代理寻找之前的进行到的最后一条所在的页数
    if lasttoken != None:
        lastpage = findPage(lastpage,lastgid,lasttoken,APIProxy)
    print("创建目录爬虫")
    # 上次进行到的页数和项目
    geter = getindex(lastpage=lastpage, toekn= lasttoken)
    while True:
        # 如果目录队列的项目小于5则开始获取下一页
        if qi.qsize() < 5:
            # 目录列表为空才会启动
            if len(indexlist) == 0:
                try:
                    # 获取到目录
                    indexlist = geter.getlist()
                except GetIndexError as e:
                    print(e)
                    break
            try:
                # 调用API爬虫
                APIdata = getAPIdata(indexlist,APIProxy)
                # 生成值对象列表
                dataOVlist = datadump(APIdata)
                # 将值对象送入队列
                for dataOV in dataOVlist:
                    if dataOV.getindex()[1] == TARGET[1]:
                        TatgetTag = True
                        break
                    # print(dataOV)
                    qi.put(dataOV)
                # 清空队列
                indexlist = []
                dataOVlist = []
            except BanIPError:
                print("API爬虫的代理已被Ban，更换代理")
                APIProxy = getIP()
            except APIError as e:
                print(e)
                break
        if TatgetTag :
            print("到达目标位置，目录发生器停止运行")
            break


def findPage(lastpage, lastgid, lasttoken, proxy):
    excookies = requests.utils.cookiejar_from_dict(COOKIE_DICT, cookiejar=None, overwrite=True)
    ehheaders = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                 'Accept-Encoding': 'gzip, deflate',
                 'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.7, ja; q=0.3',
                 'Connection': 'Keep-Alive',
                 'Host': 'exhentai.org',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
    print("开始获取上次进行到的位置")
    while True:
        try:
            html = requests.get('https://exhentai.org/?page=' + str(lastpage), headers=ehheaders, cookies=excookies, proxies = proxy).text
            if 'ExHentai.org - The X Makes It Sound Cool' not in html and 'Your IP' in html:
                proxy = getIP()
            elif lasttoken not in html:
                lastpage += 1
                print(lastpage)
                continue
            else:
                return lastpage
        except BanIPError as e:
            print(e.__str__())
            pass

def getlastindex():
    rootpath = os.path.abspath(config.__file__)
    if os.name == "nt":
        pathlist = rootpath.split("\\")
        pathlist.pop(len(pathlist) - 1)
        pathlist.append("lastpage&index.txt")
        lastindexpath = "\\".join(pathlist)

    else:
        pathlist = rootpath.split("/")
        pathlist.pop(len(pathlist) - 1)
        pathlist.append("lastpage&index.txt")
        lastindexpath = "/".join(pathlist)
    with open(lastindexpath, 'r') as f:
        lastindex = f.readline().split(',')
        if len(lastindex) == 3:
            return lastindex[0],lastindex[1], lastindex[2]
        return 0,0,None


if __name__ == "__main__":
    lastindex = [1038012,'a402646564']
    findPage(0,lastindex,config.ABS_PROXY)
