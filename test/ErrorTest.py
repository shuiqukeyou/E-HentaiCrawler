# -*- coding: utf-8 -*-
import os
import config


class GetIndexError(RuntimeError):

    def __init__(self,page,lastindex):
        self.__page = page
        self.__lastindex = lastindex

    def __str__(self):
        return '当前进行到的页数：%s,当前进行的最后一条：%s' % (str(self.__page),str(self.__lastindex))

def test():
    raise GetIndexError(2,3)

def test2():
    try:
        test()
    except GetIndexError as e:
        print(e)

def write(list):
    rootpath = os.path.abspath(config.__file__)
    if os.name == "nt":
        pathlist = rootpath.split("\\")
        pathlist.pop(len(pathlist) - 1)
        pathlist.append("lastpage&index.txt")
        lastindexpath = "\\".join(pathlist)

    else:
        pathlist = rootpath.split("/")
        pathlist.pop(len(pathlist) - 1)
        pathlist.append("lastpage&index.txt")
        lastindexpath = "/".join(pathlist)
    with open(lastindexpath, 'w') as f:
        f.write(str(list[0]) + "," + list[1])

def read():
    rootpath = os.path.abspath(config.__file__)
    if os.name == "nt":
        pathlist = rootpath.split("\\")
        pathlist.pop(len(pathlist) - 1)
        pathlist.append("lastpage&index.txt")
        lastindexpath = "\\".join(pathlist)

    else:
        pathlist = rootpath.split("/")
        pathlist.pop(len(pathlist) - 1)
        pathlist.append("lastpage&index.txt")
        lastindexpath = "/".join(pathlist)
    with open(lastindexpath, 'r') as f:
        lastindex = f.readline().split(',')
        if len(lastindex) == 2:
            return lastindex[0],lastindex[1]
        return 0,None


if __name__ == "__main__":
    a,b = read()
    print(a,b)