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