import pymysql

# 本质上是读取已有的数据，当ex值不为0时就返回数据
class getindex(object):
    def __init__(self,no = 1):
        self.__no = no
        self.__cur = self.__link_database()
        self.__n = self.__getn()

    def __link_database(self):
        return pymysql.connect(host='127.0.0.1', user='数据库帐号', passwd='数据库密码', db='ehproject', charset='utf8').cursor()

    def __getn(self):
        self.__cur.execute("select count(*) from ehindex")
        return int(self.__cur.fetchone()[0])

    def geter(self):
        i = 1
        while i <= self.__n:
            if i>= self.__no:
                self.__cur.execute("select ex from ehtest where id = " + str(i))
                ex = self.__cur.fetchone()[0]
                # ex的值
                if ex !=0 :
                    self.__cur.execute("select * from ehtest where id = " + str(i))
                    index = self.__cur.fetchone()
                    # 返回数据格式为 gid、token、id（因为事实上id这个属性是之后才加入的，所以用了这么一个别扭的方式返回数据）
                    yield [index[1], index[2], index[0]]

            i +=1
        print("所有本子已全部输出完毕")
        raise StopIteration

if __name__ == '__main__':
    test = getindex(477079).geter()
    n = 1
    l = []
    for i in test:
        l.append(i)
        n +=1
        if n>10:
            break
    print(l)
