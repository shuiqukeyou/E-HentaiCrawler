# -*- coding: utf-8 -*-
import pymysql

class writedata(object):
    def __init__(self,user,passwd,db='mysql',host='127.0.0.1'):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__db = db
        self.__conn = None
        self.__cur = self.__link_database()

    def __link_database(self):
        try:
            # 后记：早期的迷之连接手法，不过要用分布式爬虫的话其实该这么写（大概）
            self.__conn = pymysql.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db=self.__db)
            self.__conn.set_charset('utf8')
            return self.__conn.cursor()
            print('数据库连接成功')
        except pymysql.err.OperationalError as e:
            # 后记：事实上运行在本地的mysql数据库在本次爬虫中一次没有挂过，由于目录模块写的最早所以有这个东西，在之后的数据库相关模块里就再也没有了
            print('数据库连接失败')
            raise pymysql.err.OperationalError

    def write(self,data):
        try:
            self.__cur.execute('insert into ehindex (gid,token) values ("'+data[0]+'","'+data[1]+'")')
            self.__cur.connection.commit()
        except pymysql.err.OperationalError as e:
            print('写入失败')
            raise pymysql.err.OperationalError

    def exitdatabase(self):
        self.__cur.close()
        self.__conn.close()

if __name__ == "__main__":
    test = [['1020558', 'aaa0a58553'], ['1020603', '1f696b2626'], ['1020602', '3046e11a1f'], ['1020576', '90443eec25'], ['1020589', '204a87e356'], ['1020596', '149318d694'], ['1020594', '9e5be78514'], ['1020591', '8bc1425bd9'], ['1020587', '99fb00a577'], ['1020585', 'f24a4d436a'], ['1020595', '40f3763097'], ['1020590', '9713ed0653'], ['1020588', 'd26e80b2b7'], ['1020584', 'c79b39790a'], ['1020586', '1941867bf1'], ['1020582', '4679fecbff'], ['1020583', 'e386882aee'], ['1020580', 'fe47b52884'], ['1020578', 'f36f3c0e19'], ['1020579', 'caa97f7ae3'], ['1020577', 'f682ea697e'], ['1020499', 'a837595dc7'], ['1020575', 'a47934a8a0'], ['1020557', '4c50f242a4'], ['1020567', '2c69ffcd83']]
    writer = writedata('root','19941212dD','test')
    for data in test:
        writer.write(data)
    writer.exitdatabase()
