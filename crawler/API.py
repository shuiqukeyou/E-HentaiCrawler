# -*- coding: utf-8 -*-

import requests
import json
from error.error import BanIPError

'''
ehentai的API不区分表站和EX，都可以获取，甚至可以获取已被下架的本子，但由于我能获取到的本子列表全是在架的所以这个特性没有意义
每次请求最多25条
连续请求4~5次后需要等待约5秒
单线程
'''


def getdata(jsonStr, IPandport):
    posturl = "http://e-hentai.org/api.php"  # E-hentaiAPI
    jsonObj = json.dumps(jsonStr).encode("utf-8")
    proxies = {"http": "http://%s:%s" % (IPandport[0], str(IPandport[1]))}
    try:
        req = requests.post(posturl, proxies=proxies, data=jsonObj)
    except requests.exceptions.ProxyError as e:
        print('代理服务器未响应，等待10秒后重新测试')
        raise
    except ConnectionResetError:
        print(req.text)
        print('代理可能已经失效')
        raise BanIPError
    if 'This content is not available' in req.text:
        print(req.text)
        raise BanIPError
    try:
        text = (req.text).replace('\ud83d\udce4', " ")
        return json.loads(text)  # dick对象
    except json.decoder.JSONDecodeError:
        print(req.text)
        print('代理可能已经失效')
        raise BanIPError
    except requests.exceptions.ChunkedEncodingError:
        print(req.text)
        print('代理可能已经失效')
        raise BanIPError


if __name__ == "__main__":
    # 测试用数据
    jsonStr = {'method': 'gdata', 'gidlist': [[1020596, '149318d694'], [1020597, 'd1129a2aa3'], [1020598, 'f890d6c434'],
                                              [1020599, '533a889f92'], [1020600, '6eb095ac5d'], [1020601, '5f9865a41b'],
                                              [1020602, '3046e11a1f'], [1020603, '1f696b2626'], [1020609, '7df75786ee'],
                                              [1020610, '957fe008d6'], [1020611, '2dea1d8517'], [1020612, '31a75cce4a'],
                                              [1020613, 'c4e73ed2ce'], [1020617, '2d4efd6e91']], 'namespace': 1}
    # 这是个不可用的代理，实际项目运行中，这里使用了我的VPS自建的代理
    IPandport = ['127.0.0.1', 25]
    print(getdata(jsonStr, IPandport))
