
from crawler.ehread import getfav_rat
from time import sleep
from error.error import ProxyError,IsExHon
from Proxy.IPPool import getIP

# 循环检查目录队列（qi），如果目录队列有数据则将其传入getfav_rat方法，将获取到的数据传入数据队列中（qd），如果发生错误，将数据传入错误队列中（qe）
def dataget(qi,qd,qe,px):
    count = 0
    try:
        ProxyErrorCount = 0
        while True:
            if qi.empty():
                sleep(1)
            else:
                while True:
                    index = qi.get()
                    id = index[2]
                    try:
                        data = getfav_rat(index[0],index[1],px)
                        sleep(0.5)
                        data.append(id)
                        qd.put(data)
                        print(data)
                        count +=1
                        ProxyErrorCount = 0
                    except IsExHon:
                        print("这个本子是EX的，跳过")
                        break
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
        # 向错误队列中输入当前使用的代理、当前进行到的项目、id
        errordata = [px,index,id]
        qe.put(errordata)

