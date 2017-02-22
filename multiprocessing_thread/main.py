from multiprocessing import Process,Queue
from multiprocessing_thread.index_get import index_get
from multiprocessing_thread.data_write import read
from multiprocessing_thread.data_get import dataget
from multiprocessing_thread.error_handling import error_handing
from time import sleep
from Proxy.IPPool import getIP
import threading
from error.error import IPPoolEmpError

def datagettest(qi,qd):
    while True:
        if qi.empty():
            sleep(1)
        else:
            qd.put(qi.get())

if __name__=='__main__':
    # 目录队列
    qindex = Queue()
    # 数据队列
    qdata = Queue()
    # 错误队列
    qerror = Queue()
    # ip队列
    qip = Queue()
    threading.Thread(target=index_get, args=(qindex, 444679)).start()
    threading.Thread(target=read, args=(qdata,)).start()
    # 先行启动两个爬虫进程，每个进程最多开启10个线程
    Process(target=dataget, args=(qindex, qdata, qerror, qip)).start()
    Process(target=dataget, args=(qindex, qdata, qerror, qip)).start()
    n = 0
    # 最多获取20个IP
    while n < 20:
        try:
            # 每获取到一个代理就会将其送入到代理队列中
            qip.put(getIP())
            n+=1
        except BaseException:
            break
    threading.Thread(target=error_handing, args=(qdata, qerror, qip,n)).start()
