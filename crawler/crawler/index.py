# -*- coding: utf-8 -*-
'''
这个类为获取本子列表的爬虫
传入参数为中断时的页码，如果没有传入，则从第一页开始
如果获取成功，返回结果为一个由本子地址关键字构成的list和上次结果的最后一个值（当ex上有新本子上传时，所有本子的顺序会往后挪动）
如果获取失败，返回结果为这次的页数和上结果的最后一个值，用于重启动爬虫
'''
import re
import os
from time import sleep

import requests
from bs4 import BeautifulSoup

import config
from error.error import ExOpenError,BanIPError,GetIndexError
from Proxy.IPPool import getIP


class getindex(object):
    def __init__(self, lastpage=0, toekn = None):
        self.__lastpage = lastpage  # 当前进行到第几页
        self.__token = toekn  # 上一页的最后一条
        self.__excookies = requests.utils.cookiejar_from_dict(config.COOKIE_DICT, cookiejar=None, overwrite=True)# 装载cookie
        self.__IPandport = getIP()
        self.__proxies = {"https": "http://%s:%s"%(self.__IPandport[0],str(self.__IPandport[1]))}
        print("目录爬虫启动")


    # 返回结果
    def getlist(self):
        print("目录爬虫进行到第%s"%self.__lastpage)
        return self.__read_html()
        # print(self.__read_html())

    # 解析获取到的网页
    def __read_html(self):
        hlist = []
        ErrorCount = 0
        while True:
            try:
                bsobj = BeautifulSoup(self.__open_next())
                table = bsobj.find('table', {'class': 'itg'})
                for link in table.findAll('a', href=re.compile('https://exhentai\.org/g/[0-9]{1,8}/[A-Za-z0-9]{10}/')):
                    if 'href' in link.attrs:
                        hlist.append(self.__parse_html(link.attrs['href']))
                #  检查上一页的最后一条有没有被挤到这页，如果有，修剪目录list
                if self.__token in hlist:
                    lastindex = hlist.index(self.__token)
                    hlist = hlist[lastindex+1:len(hlist)]
                # 更新最后一条的值
                self.__token = hlist[-1]
                # 写入最后一条的值
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
                with open(lastindexpath, 'w') as f:
                    f.write(str(self.__lastpage) + "," + str(self.__token[0]) + ',' + self.__token[1])
                self.__lastpage += 1
                return hlist
            except BaseException as e:
                print("列表爬虫发生未知异常,重新尝试获取列表")
                print("异常信息：", e.__str__())

                rootpath = os.path.abspath(config.__file__)
                if os.name == "nt":
                    pathlist = rootpath.split("\\")
                    pathlist.pop(len(pathlist) - 1)
                    pathlist.append("Log.txt")
                    logpath = "\\".join(pathlist)

                else:
                    pathlist = rootpath.split("/")
                    pathlist.pop(len(pathlist) - 1)
                    pathlist.append("Log.txt")
                    logpath = "/".join(pathlist)
                with open(logpath, 'a') as f:
                    f.write("列表爬虫异常：" + e.__str__())
                ErrorCount += 1
            if ErrorCount > 5:
                self.__IPandport = getIP()
                self.__proxies = {"https": "http://%s:%s" % (self.__IPandport[0], str(self.__IPandport[1]))}

    # 解析连接为list，用于之后组装JSON
    def __parse_html(self, link):
        return (link.split('/')[4:6])

    # 检查打开ex站的结果
    def __open_next(self):
        ErrorCount = 0
        while True:
            try:
                return self.__open_Ex(self.__excookies, exurl='https://exhentai.org/?page=' + str(self.__lastpage))
            except ExOpenError :
                print("代理姨妈或者E绅士服务器姨妈，等待5秒后重试")
                ErrorCount +=1
                sleep(5)
            except BanIPError:
                print()
                print("目录爬虫的IP已被Ban，更换IP")
                self.__proxies = getIP()
            except BanIPError as e:
                print("发生未知错误，等待5秒后重试")
                print("错误输出：", e.__str__())
                ErrorCount += 1
                sleep(5)
            if ErrorCount  >= 10:
                print("目录获取失败超过10次，更换IP")
                self.__proxies = getIP()


    # 打开exhentai，如果访问异常，或者吃了熊猫或是被ban了IP，就会抛出错误
    def __open_Ex(self,cookie, exurl='https://exhentai.org/'):
        ehheaders = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                     'Accept-Encoding': 'gzip, deflate',
                     'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.7, ja; q=0.3',
                     'Connection': 'Keep-Alive',
                     'Host': 'exhentai.org',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
        # print("开始尝试获取列表")
        html = requests.get(exurl, headers=ehheaders, cookies=cookie, proxies = self.__proxies).text
        if 'ExHentai.org - The X Makes It Sound Cool' in html:
            return html
        elif 'Your IP' in html:
            raise ExOpenError
        else:
            raise BanIPError


if __name__ == "__main__":
    opentest = getindex()
    i = 0
    while i<10:
        print(opentest.getlist())
        print("--*--*--")
        i+=1
