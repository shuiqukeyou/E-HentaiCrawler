from  time import sleep

import pymysql
from pymysql.err import MySQLError

# 与多进程版本无异
def read(qd):
    print('数据写入器启动')
    while True:
        if qd.empty():
            pass
        else:
            v = qd.get()
            writedata(v[0],v[1],v[2],v[3],v[4])
            # print(v)

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='数据库密码', db='ehproject',charset='utf8')
cur = conn.cursor()  # 光标对象

# 事实上在整个项目进行中，数据库结构做了很多次调整，所以这里用了一个独立的写入函数

def writedata(fav,rat,jtitle,language,id):
    if len(jtitle)!=0:
        jtitle = jtitle.replace('📤','')
        sql = "update ehdata set Favorited = %s,Ratings = %s,title_jpn = '%s',language = '%s',ex='1'，writed='1' where id = %s"%(fav,rat,jtitle,language,id)
        try:
            print(sql)
            cur.execute(sql)
        except BaseException:
            print("写入失败，sql语句已写入日志文件,请检查mysql语句")
            print(sql)
            sqltxt(sql)
    else:
        sql = "update ehdata set Favorited = %s,Ratings = %s,language = '%s',ex = 1，writed='1' where id = %s" % (fav, rat,language,id)
        try:
            print(sql)
            cur.execute(sql)
        except MySQLError:
            print("写入失败，sql语句已写入日志文件,请检查mysql语句")
            print(sql)
            try:
                sqltxt(sql)
            except BaseException:
                print("发生未知错误，请自行在记录中搜索")
    cur.connection.commit()


def sqltxt(sql):
    # 更稳妥的办法是用os模块获取当前目录然后在目录下生产错误日志文件，然而我懒..
    with open('E:/sqlstr.txt',"a") as s:
        s.write(sql)
        s.write("\n")

