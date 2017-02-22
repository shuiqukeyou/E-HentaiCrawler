from time import sleep
from Proxy.IPPool import testIP,getIP
from error.error import ProxyInvaError,IPPoolEmpError,IPProxyPoolRunError
from crawler.exread import getfav_rat
# 备用代理
PX = ['127.0.0.1',25]

# 与多进程版本几乎无异，只是线程重启从这里移动到了爬虫进程中

def error_handing(qd, qe, qip, n):
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
                index = ve[1]
                id= ve[2]
                data = getfav_rat(index[0], index[1], PX)
                data.append(id)
                qd.put(data)
                print("错误处理：%s" % id)
                n -= 1
        else:
            sleep(1)
            # 每三分多钟检查一次IP池
            count = int((count+1)%180)
        if  count == 0 :
            n = reProcess(qip,n)

# 重启线程的工作不再在错误处理进程里进行，而是直接向代理队列输入新获取到的可用代理，由爬虫进程自行开启线程
def reProcess(qip,n):
    if n<20:
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

