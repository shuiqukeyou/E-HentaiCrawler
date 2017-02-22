from  time import sleep

import pymysql
from pymysql.err import MySQLError

# 检查data队列，如果有，就写入数据库
def read(qd):
    print('数据写入器启动')
    while True:
        if qd.empty():
            pass
        else:
            v = qd.get()
            writedata(v[0],v[1],v[2],v[3])

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='数据库密码', db='ehproject',charset='utf8')
cur = conn.cursor()  # 光标对象

def writedata(fav,rat,jtitle,id):
    if len(jtitle)!=0:
        jtitle = jtitle.replace('📤','')
        sql = "update ehdata set Favorited = %s,Ratings = %s,title_jpn = '%s',ex= 0 where id = %s"%(fav,rat,jtitle,id)
        try:
            print(sql)
            cur.execute(sql)
        except BaseException:
            print("写入失败，sql语句已写入日志文件,请检查mysql语句")
            print(sql)
            sqltxt(sql)
    else:
        sql = "update ehdata set Favorited = %s,Ratings = %s,ex = 0 where id = %s" % (fav, rat,id)
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
    with open('E:/sqlstr.txt',"a") as s:
        s.write(sql)
        s.write("\n")

