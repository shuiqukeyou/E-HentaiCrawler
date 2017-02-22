from database.read.getindex import getindex

def index_get(qi,i=1):
    print('index队列生成器启动')
    # 调用了之前的getindex方法
    indexs = getindex(i).geter()
    # 只要目录队列的数据小于等于8个，就开始向目录队列中输入新数据
    for i in indexs:
        while True:
            if qi.qsize()<=8:
                qi.put(i)
                break
