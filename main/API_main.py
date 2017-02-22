import logging
from time import sleep

import requests
from crawler.API import getdata
from database.read.getindex import getindex
from database.write.API import writedata
from Proxy.IPPool import getIP
from error.error import BanIPError
from ehemail.ehemail import remind
from error.error import IPPoolEmpError,IPProxyPoolRunError


# 被ban的IP
banedIPlist = []
# 后记：真是MyIPandport系列啊，不是跟风Myxx什么的..毕竟是我自己的VPS..
MyIPandport = ['127.0.0.1',25,]

# 后记：天知道我那时候为什么用了这么个函数名
# 后记：论面向过程编程
def go(id=1,IPandport = MyIPandport):
    x=0
    i = 0
    # 目录数计数
    indexcount = 0
    # json语句变量
    indexlist = []
    # 代理错误计数
    proxycount = 0
    IPandport = getIP()
    jsonStr = {"method": "gdata", "gidlist": indexlist, "namespace": 1}
    geter = getindex(id).geter()
    try:
        for index in geter:
            indexlist.append([index[0],index[1]])
            indexcount +=1
            # print(index)
            while indexcount == 25:
                try:
                    datajson = getdata(jsonStr,IPandport)
                    id = writedata(datajson,id)
                    print('已写入%s'%(id-1))
                    i += 1
                    indexcount = 0 # 如果写入成功，重置目录计数
                    indexlist = [] # 如果写入成功，重置目录列表
                    jsonStr = {"method": "gdata", "gidlist": indexlist, "namespace": 1}
                    proxycount = 0 # 如果写入成功，重置代理测试计数
                except requests.exceptions.ProxyError as e:
                    proxycount +=1
                    sleep(10)
                    print(e.__str__())
                except BanIPError as e:
                    print('%s该代理已经被ban，更换代理'%(IPandport[0]))
                    banedIPlist.append(IPandport[0])
                    IPandport = changeproxies()
                    proxycount = 0# 重置代理计数
                except ConnectionResetError:
                    print('%s该代理已经被ban，更换代理'%(IPandport[0]))
                    banedIPlist.append(IPandport[0])
                    IPandport = changeproxies()
                    proxycount = 0# 重置代理计数
                if proxycount == 3:
                    print('当前代理已连续三次失效，更换代理')
                    IPandport = changeproxies()
                    proxycount = 0# 重置代理计数

            if i ==5 :
                sleep(6)
                i = 0

        if len(indexlist) !=0 and len(indexlist) !=25:
            try:
                datajson = getdata(jsonStr, IPandport)
                id = writedata(id,datajson)
                indexcount = 0  # 如果写入成功，重置目录计数
                indexlist = []  # 如果写入成功，重置目录列表
                jsonStr = {"method": "gdata", "gidlist": indexlist, "namespace": 1}
                proxycount = 0  # 如果写入成功，重置代理测试计数
            except requests.exceptions.ProxyError as e:
                proxycount += 1
                print(e.__str__())
            except BanIPError as e:
                banedIPlist.append(IPandport[0])
                IPandport = changeproxies()
                proxycount = 0  # 重置代理计数
            if proxycount == 3:
                print('当前代理已连续三次失效，更换代理')
                IPandport = changeproxies()
                proxycount = 0  # 重置代理计数

    except BaseException as e:
        print('发生未知错误')
        logging.exception(e)
        print(id)
        print(jsonStr)
        remind('程序异常终止')



def changeproxies():
    try:
        IPandport = getIP()
    except IPProxyPoolRunError as e:
        IPandport = MyIPandport
    except IPPoolEmpError as e:
        IPandport = MyIPandport
    if IPandport[0] in banedIPlist and IPandport[0] == '144.168.63.75':
        print('已无任何可用IP')
        raise NOIPError
    return IPandport

class NOIPError (RuntimeError):
    pass

go(455351)