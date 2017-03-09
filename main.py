# -*- coding: utf-8 -*-
import threading
from multiprocessing import Queue, Process

from Proxy.IPPool import getIP
from config import PROCESS_MAX, THREAD_MAX
from crawler.indexgeter import indexgeter
from crawler.webDataGeter import webdatageter
from database.data_writer import data_writer
from error.error_handling import error_handing

if __name__ == "__main__":
    # 目录队列
    qindex = Queue()
    # 数据队列
    qdata = Queue()
    # 错误队列
    qerror = Queue()
    # 代理队列
    qip = Queue()
    # 启动目录发生器进程
    Process(target=indexgeter, args=(qindex,)).start()
    # 开始启动爬虫进程
    n = 0
    while n < PROCESS_MAX:
        Process(target=webdatageter, args=(qindex, qdata, qerror, qip)).start()
        n += 1
    # 数据写入器线程
    threading.Thread(target=data_writer, args=(qdata,)).start()
    # 错误处理线程
    threading.Thread(target=error_handing, args=(qdata, qerror, qip, n)).start()
    # 获取THREAD_COUNT个代理用于开启爬虫线程
    n = 0
    while n < THREAD_MAX * THREAD_MAX:
        try:
            qip.put(getIP())
            n += 1
        except BaseException:
            break

