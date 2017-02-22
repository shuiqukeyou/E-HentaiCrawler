# -*- coding: utf-8 -*-

import pymysql

# 新建记录目录的的数据库

def newtable():
    with pymysql.connect(host='127.0.0.1', user='数据库帐号', passwd='数据库密码', db='mysql') as  conn:
        conn.execute('create database if not exists ehproject')
        conn.execute('use ehproject')
        conn.execute('create table ehindex(gid int(7) not null,token char(10) not null)')
