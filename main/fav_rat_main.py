import logging
from time import sleep

from Proxy.IPPool import getIP
from crawler.exread import BanIPError,ExPandaError,ProxyError
from crawler.exread import getfav_rat
from database.read.getindex import getindex
from database.write.fav_rat import writedata
from ehemail.ehemail import remind

# 后记：还是面向过程编程，基本结构和API的主函数一样，但是由于这里不需要像API部分那样每25条数据一次发送一次，所以简短了不少
# 后记：仍然是单线程、无代理切换，但是在这里我被banIP ban到死，最后做了代理+多线程版。

def go(no=1):
    IPandport = ['104.196.177.247', 80, ]
    indexs = getindex(no).geter()
    proxycount = 0
    count = 0
    try:
        for index in indexs:
            while True:
                try:
                    id = index[2]
                    data = getfav_rat(index[0],index[1],IPandport)
                    writedata(data[0],data[1],data[2],id)
                    sleep(0.5)
                    count +=1
                    no+=1
                    proxycount = 0
                    break
                except ProxyError:
                    proxycount +=1
                    sleep(5)
                except ExPandaError:
                    raise
                except BanIPError:
                    IPandport = getIP()
                    proxycount = 0
                if proxycount >=5:
                    IPandport = getIP()
                    proxycount = 0
            # 每拿到100条数据，暂停十秒
            if count == 100:
                sleep(10)
                count = 0
    except BaseException as e:
        print('发生未知错误')
        # 发生错误时，输出错误信息、当前所用的no、id、代理
        logging.exception(e)
        print(no)
        print(id)
        print(IPandport)
        remind('程序异常终止')



# IPandport=
go(18047)