import pymysql

class getindex(object):
    def __init__(self,no = 1):
        self.__no = no
        self.__cur = self.__link_database()
        self.__n = self.__getn()

    # 连接数据库
    def __link_database(self):
        return pymysql.connect(host='127.0.0.1', user='数据库帐号', passwd='数据库密码', db='ehproject', charset='utf8').cursor()

    #  获取目录条目数
    def __getn(self):
        self.__cur.execute("select count(*) from ehindex")
        return int(self.__cur.fetchone()[0])

    # 返回一个目录值
    def geter(self):
        i = 1
        while i <= self.__n:
            if i>= self.__no:
                self.__cur.execute("select * from ehindex where id = " + str(i))
                yield self.__cur.fetchone()
            i +=1
        raise StopIteration

if __name__ == '__main__':
    test = getindex(18047).geter()
    n = 1
    l = []
    for i in test:
        l.append(i)
        n +=1
        if n>1:
            break
    print(l)
