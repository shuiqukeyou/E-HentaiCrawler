# -*- coding: utf-8 -*-

# IPProxyPool相关错误
class IPProxyPoolRunError(RuntimeError):
    pass

class IPPoolEmpError(RuntimeError):
    pass

class ProxyInvaError(RuntimeError):
    pass

# E绅士相关错误
class ExOpenError(RuntimeError):
    pass
class BanIPError(RuntimeError):
    pass
class ExPandaError(RuntimeError):
    pass
class IsExHon(RuntimeError):
    pass

# 网络相关错误
class ProxyError(RuntimeError):
    pass

class GetIndexError(RuntimeError):

    def __init__(self,page,lastindex):
        self.__page = page
        self.__lastindex = lastindex

    def __str__(self):
        return '当前进行到的页数：%s,当前进行的最后一条：%s' % (str(self.__page),str(self.__lastindex))

class APIError(RuntimeError):

    def __init__(self,json):
        self.__json = json

    def __str__(self):
        return ('当前发生异常的JSON语句：%s'% self.__json)