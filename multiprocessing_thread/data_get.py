import threading
from crawler.exread import getfav_rat
from time import sleep
from error.error import ProxyError
from Proxy.IPPool import getIP

# 基本结构仍然是面向过程编程流

def __dataget(qi,qd,qe,px,n):
    lock = threading.Lock()
    count = 0
    try:
        ProxyErrorCount = 0
        while True:
            if qi.empty():
                sleep(1)
            else:
                while True:
                    lock.acquire()
                    try:
                        index = qi.get()
                    finally:
                        lock.release()
                    id = index[2]
                    try:
                        data = getfav_rat(index[0],index[1],px)
                        sleep(0.5)
                        data.append(id)
                        lock.acquire()
                        try:
                            qd.put(data)
                        finally:
                            lock.release()
                        count +=1
                        ProxyErrorCount = 0
                    except ProxyError:
                        ProxyErrorCount +=1
                        sleep(10)
                    if ProxyErrorCount >=10:
                        # 代理连续错误十次则更换IP
                        print("更换IP")
                        px = getIP()
                        ProxyErrorCount = 0
                    if count >=100:
                        sleep(10)
    # 如果发生任何不能处理的错误（没有代理、熊猫等），向错误队列内输出当前使用的代理和当前数据
    except BaseException as e:
        print(e.__str__())
        n -= 1
        errordata = [px,index,id]
        qe.put(errordata)

def dataget(qi,qd,qe,qip):
    n = 0
    print('爬虫进程启动')
    while True:
        # 线程数低于10时，就会淦TM的线程开爆
        while n<10 and not qip.empty():
            n += 1
            threading.Thread(target=__dataget, args=(qi, qd, qe, qip.get(),n)).start()

def erha(qi,qd,qe,qip):
    while True:
        if not qi.empty():
            threading.Thread(target=__dataget, args=(qi, qd, qe, qip.get())).start()

