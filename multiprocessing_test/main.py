from multiprocessing import Process,Queue
from multiprocessing_test.index_get import index_get
from multiprocessing_test.data_write import read
from multiprocessing_test.data_get import dataget
from multiprocessing_test.error_handling import error_handing
from Proxy.IPPool import getIP
import threading

'''
后记：目录、数据处理、错误处理作为三个线程在主进程里启动
爬虫作为子进程启动
但事实上并没有对爬虫进程做任何控制，如果不是在PyCharm中运行，可能会有僵尸进程的问题
另外我的爬虫进程仍然是单进程单线程的，爬虫这种IO阻塞很严重的工作这么做效率很低
事实上就是因为我的电脑风扇声大到快要爆炸..我才写了多线程版本。
'''

if __name__=='__main__':
    # 目录队列
    qindex = Queue()
    # 数据队列
    qdata = Queue()
    # 错误队列
    qerror = Queue()
    threading.Thread(target=index_get, args=(qindex, 197078)).start()
    threading.Thread(target=read, args=(qdata,)).start()
    n = 0
    # 最多启动四个爬虫进程
    while n<4:
        try:
            Process(target=dataget, args=(qindex, qdata, qerror, getIP())).start()
            n+=1
        except  BaseException:
            break
    threading.Thread(target=error_handing, args=(qindex, qdata, qerror,n)).start()


