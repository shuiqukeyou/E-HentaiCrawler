from database.read.getExIndex import getindex

# 大概是一字未改
def index_get(qi,i=1):
    print('index队列生成器启动')
    indexs = getindex(i).geter()
    for i in indexs:
        while True:
            if qi.qsize()<=8:
                qi.put(i)
                break
