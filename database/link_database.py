# -*- coding: utf-8 -*-

import pymysql
import config

database_log_config = config.DATABASE_LOGIN_CONFIN

def link_database(fun,database_log_config = database_log_config):
    def wr(*args,**kw):
        with pymysql.connect(host = database_log_config['host'], user = database_log_config['user'],
                               passwd = database_log_config['passwd'], db = database_log_config['db'],
                               charset = database_log_config['charset']) as cur:
            fun(cur, *args, **kw)
    return wr

if __name__ == '__main__' :
    @ link_database
    def test(cur,str):
        print(type(cur))
        print(type(str))

    test("s")
