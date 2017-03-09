# -*- coding: utf-8 -*-
import threading
from time import sleep

from Proxy.IPPool import getIP
from config import THREAD_MAX
from crawler.crawler.exread import getfav_rat
from error.error import ProxyError


def __dataget(qi,qd,qe,px,n):
    count = 0
    try:
        ProxyErrorCount = 0
        while True:
            if qi.empty():
                sleep(1)
            else:
                while True:
                    data = qi.get()
                    try:
                        index = data.getindex()
                        webdata = getfav_rat(index[0], index[1], px)
                        data.update(favorited = webdata['favorited'], ratings = webdata['ratings'], elanguage = webdata['elanguage'], title_jpn = webdata['title_jpn'])
                        sleep(0.5)
                        qd.put(data)
                        count +=1
                        ProxyErrorCount = 0
                    # 爬取EX本子时，404错误全为代理服务器抛出的
                    except ProxyError:
                        ProxyErrorCount +=1
                        sleep(10)
                    if ProxyErrorCount >=10:
                        # 代理连续错误十次则更换IP
                        print("更换爬虫IP")
                        px = getIP()
                        ProxyErrorCount = 0
                    if count >=100:
                        sleep(10)
    # 如果发生任何不能处理的错误（没有代理、熊猫等），向错误队列内输出当前使用的代理和当前数据
    except BaseException as e:
        print("爬虫进程发生未知错误：",e.__str__())
        n -= 1
        errordata = [px, data]
        qe.put(errordata)

def webdatageter(qi, qd, qe, qip):
    n = 0
    while True:
        while n < THREAD_MAX and not qip.empty():
            print('爬虫线程启动')
            n += 1
            threading.Thread(target=__dataget, args=(qi, qd, qe, qip.get(),n)).start()
