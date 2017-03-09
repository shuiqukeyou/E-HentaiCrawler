# -*- coding: utf-8 -*-
import requests
import json
import os
from time import sleep

import config
from error.error import BanIPError,APIError



'''
ehentai的API不区分表站和EX，都可以获取，甚至可以获取已被下架的本子，但由于能获取到的本子列表全是在架的所以这个特性没有意义
每次请求最多25条
连续请求4~5次后需要等待约5秒
'''


def getAPIdata(jsonStr,IPandport):
    posturl = "https://e-hentai.org/api.php"#E-hentaiAPI
    jsonObj = json.dumps(index2json(jsonStr)).encode("utf-8")
    proxies = { "https": "http://%s:%s"%(IPandport[0],str(IPandport[1]))}
    ErrorCount = 0
    while True:
        try:
            req = requests.post(posturl,proxies=proxies,data=jsonObj)
            html = (req.text).replace('\ud83d\udce4', " ")
            if 'Your IP' in html:
                print(html)
                raise BanIPError
            try:
                return json.loads(html)  # dick对象
            except BaseException as e:
                print('API爬虫发生未知错误，终止API爬虫,已输出错误信息到日志文件')
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
                    f.write("API爬虫异常：" + e.__str__())
                raise APIError(html)
        except BaseException as  e:
            print(e.__str__())
            ErrorCount += 1
            if ErrorCount > 5:
                raise BanIPError
            print('代理服务器未响应，等待5秒后重新尝试')
            sleep(5)


def index2json(list):
    list2 = []
    for index in list:
        list2.append([int(index[0]),index[1]])
    return ({'method': 'gdata', 'gidlist': list2, 'namespace': 1})

if __name__ == "__main__":
    #测试用数据
    jsonStr = [[1020596, '149318d694'], [1020597, 'd1129a2aa3'], [1020598, 'f890d6c434'], [1020599, '533a889f92'], [1020600, '6eb095ac5d'], [1020601, '5f9865a41b'], [1020602, '3046e11a1f'], [1020603, '1f696b2626'], [1020609, '7df75786ee'], [1020610, '957fe008d6'], [1020611, '2dea1d8517'], [1020612, '31a75cce4a'], [1020613, 'c4e73ed2ce'], [1020617, '2d4efd6e91']]
    IPandport = config.ABS_PROXY
    print(getAPIdata(jsonStr,IPandport))