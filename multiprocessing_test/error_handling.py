from Proxy.IPPool import testIP,getIP
from error.error import ProxyInvaError,IPPoolEmpError,IPProxyPoolRunError
from multiprocessing import Process
from multiprocessing_test.data_get import dataget
from crawler.exread import getfav_rat

# 一个几乎绝对可用的代理，用于错误处理无法重启进程时处理剩余数据
PX = ['127.0.0.1',25]

# 循环检查错误队列
def error_handing(qi,qd,qe,n=0):
    i = 0
    print('错误处理进程启动')
    while True:
        if not qe.empty():
            ve = qe.get()
            try:
                # 调用changeip方法检查这个错误信息的ip，总是返回可用IP
                IPandport = changeip(ve[0])
                # 重启一个进程
                Process(target=dataget, args=(qi,qd,qe,IPandport)).start()
            except BaseException:
                print("无法重启爬虫进程或IP池工作状态有问题，进入终止模式，处理当前剩余数据，不再创建新进程")
                index = ve[1]
                id = ve[2]
                data = getfav_rat(index[0], index[1],PX)
                data.append(id)
                qd.put(data)
                print("错误处理：%s"% id)
                # 无法重启时，n-1
                n-=1
        # 每轮循环刷新当前进程（n）数
        n = reProcess(qi,qd,qe,n)

def reProcess(qi,qd,qe,n):
    if n<3:
        try:
            IPandport = getIP()
            print("获取到了一个新的可用IP，启动一个进程")
            n += 1
            Process(target=dataget, args=(qi, qd, qe, IPandport)).start()
            # 成功新开进程是，n+1
            n+=1
        except IPPoolEmpError:
            pass
        except IPProxyPoolRunError:
            print("IPProxyPoolRunError")
            pass
    return n


def changeip(IPandport):
    i = 0
    while i<5:
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
