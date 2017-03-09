# -*- coding: utf-8 -*-
from time import sleep

from Proxy.IPPool import testIP,getIP
from config import THREAD_MAX,ABS_PROXY
from crawler.crawler.exread import getfav_rat
from error.error import ProxyInvaError,IPPoolEmpError,IPProxyPoolRunError

def error_handing( qd, qe,qip,n):
    print('错误处理进程启动')
    count = 0
    while True:
        if not qe.empty():
            ve = qe.get()
            try:
                IPandport = changeip(ve[0])
                # 将更新的ip送回ip队列
                qip.put(IPandport)
            except BaseException:
                print("无法重启爬虫线程或IP池工作状态有问题，进入终止模式，处理当前剩余数据，不再创建新进程")

                APIdata = ve[1]
                index = APIdata.getindex()
                data = getfav_rat(index[0], index[1], ABS_PROXY)
                APIdata.update(favorited=data['favorited'], ratings=data['ratings'], elanguage=data['elanguage'],
                               title_jpn=data['title_jpn'])
                qd.put(APIdata)
                n -= 1
        else:
            sleep(1)
            # 每三分多钟检查一次IP池
            count = int((count+1)%180)
        if  count == 0 :
            n = reProcess(qip,n)

def reProcess(qip,n):
    # 如果实际启动的线程低于设定值，错误处理进程会反复尝试获取新IP，所以不要把线程数开太高
    if n<THREAD_MAX:
        while True:
            print("开始尝试重启爬虫线程")
            try:
                IPandport = getIP()
                print("获取到了一个新的可用IP")
                n += 1
                qip.put(IPandport)
                if n>=10:
                    break
            except IPPoolEmpError:
                print("IP池已空")
                break
            except IPProxyPoolRunError:
                print("IPProxyPoolRunError")
                break
    return n

def changeip(IPandport):
    i = 0
    while i<3:
        try:
            # 如果原代理还能使用，继续使用原代理
            testIP(IPandport)
            return IPandport
        except ProxyInvaError:
            i+=1
    try:
        #如果原代理已不能使用，更换IP
        return getIP()
    except IPPoolEmpError:
        print("IP池已空，启动备用IP完成已分配的任务")
        raise

