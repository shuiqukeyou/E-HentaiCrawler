# -*- coding: utf-8 -*-
from database.link_database import link_database
from objectvalue.dataOV import dataOV
import config
import os


# @link_database
def writedata(cur,webdata):
    try:
        print(webdata.getindex())
        cur.execute(webdata.getSQLStr())
        # pass
    except BaseException as e:
        print("数据写入出现异常，异常语句及异常信息已输出至SQLErrorLog.txt")
        rootpath = os.path.abspath(config.__file__)
        if os.name == "nt":
            pathlist = rootpath.split("\\")
            pathlist.pop(len(pathlist) - 1)
            pathlist.append("SQLerrorLog.txt")
            logpath = "\\".join(pathlist)

        else:
            pathlist = rootpath.split("/")
            pathlist.pop(len(pathlist) - 1)
            pathlist.append("SQLerrorLog.txt")
            logpath = "/".join(pathlist)
        with open(logpath, 'a') as f:
            try:
                f.write("异常语句："+webdata.getSQLStr())
                f.write("异常信息："+e.__str__())
            except BaseException as e:
                print("写入失败")
                print("异常语句："+webdata.getSQLStr())
                print ("异常信息："+e.__str__())
    cur.connection.commit()

if __name__ == "__main__":
    web = dataOV(gid = 1690, token ="e51461118c", favorited = 641, rating = 14, elanguage ="japanese", title_jpn ="(サンクリ34) [SAZ (己即是空, soba, 双九朗)] なChuらる★ろりぽっ！！ (魔法少女リリカルなのはA\\')")
    writedata(web)



