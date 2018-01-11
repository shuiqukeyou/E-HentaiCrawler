# -*- coding: utf-8 -*-
import requests
import json
from time import sleep

from error.error import ProxyInvaError, IPPoolEmpError, IPProxyPoolRunError, BanIPError
URL = 'http://e-hentai.org/api.php'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch, br',
          'Accept-Language': 'zh-CN,zh;q=0.8',
          'Connection': 'keep-alive',
          'DNT': '1',
          'Host': 'e-hentai.org',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
jsonStr = {'method': 'gdata', 'gidlist': [[186384, '8ee236ef21'], [186385, '5092696655'], [186387, 'c32a66c441'], [186392, 'aed2538d37'], [186393, '3d059ee6a9'], [186394, '664c6a2ee9'], [186396, '62f5688776'], [186397, '0330f4517f'], [186400, '43fd5a5df6'], [186401, '69937d6114'], [186402, '4a51c9f653'], [186403, 'cca2dbb1d7'], [186404, '314e1498f4'], [186405, '0c868ac752'], [186406, '872f123996'], [186407, 'f6d650e813'], [186409, '7f04a84e8e'], [186410, 'dd0ccd3953'], [186412, '054ec3ab43'], [186413, 'c565802b49'], [186421, '83de9bedc1'], [186424, '0f7b959cbf'], [186426, '820f4f344d'], [186429, 'c68a8ecbb4'], [186430, 'edcb7c64e2']], 'namespace': 1}

jsonObj = json.dumps(jsonStr).encode("utf-8")


# 获取一个IP
'''
三个结果：1.返回一个IPandport，2.抛出IP池已空错误，3.抛出IPProxyPool运行错误
'''
def getIP():
    i = 0
    while True:# 循环到给出一个IP或者抛出错误为止
        try:
            IPandport = getip_from_pool()
            ip = testIP(IPandport)
            i = 0
            delIP(ip)
            return ip[0:2]
        except ProxyInvaError as e:# 如果IP不可用，最多测试三次，三次如果都是失败则舍弃该IP，并重置计数器
            print('5秒后重新进行测试')
            sleep(5)
            i+=1
            if i >=5:
                print('已重复测试五次，删除该IP')
                delIP(IPandport)
                i = 0
        except BanIPError:
            print('删除该IP')
            delIP(IPandport)



# 删除一个已经被ban或者已经失效的一个IP
def delIP(ip):
    try:
        # 如果成功删除或者不成功删除（那个IP被IPProxyPool的自动检测给干掉了之类的），都意味着那个IP不在了
        # 返回值为200
        # 本地服务器5秒还没给回应的话大概是死了
        if ((requests.get('http://127.0.0.1:8000/delete?ip=%s'%(ip[0]),timeout = 5)).status_code) == 200:
            print('删除IP成功')
        else:
            print('删除IP失败')
    except BaseException as e:
        print('从IP池里删除失效IP失败，请检查IPProxyPool是否还在运行')
        raise IPProxyPoolRunError


# 测试IP是否可到达e绅士
def testIP(IPandport):
    print('测试代理%s'%(IPandport))
    if len(IPandport) == 0:# 如果返回IP为空，则IP池已空
        raise IPPoolEmpError
    proxies = {'http':'http://%s:%s'%(IPandport[0],IPandport[1])}# 组装代理
    try:
        r = requests.post(URL,headers=headers,proxies=proxies ,data=jsonObj,timeout = 5)# 组装请求
    except BaseException :
        print('代理服务器不可用或响应时间过长')
        raise ProxyInvaError
    html = r.text
    if 'This content is not available' in html:
        print("获得了一个俄罗斯代理")
        raise BanIPError
    print('代理通过测试')
    return IPandport #返回IP

#获取一组代理，并返回最靠前的那个
def getip_from_pool():
    try:
        return requests.get('http://127.0.0.1:8000/?protoco=2&count=1&country=%E5%9B%BD%E5%A4%96 ',
                            timeout = 5).json()[0]
    except BaseException:
        try:
            return requests.get('http://127.0.0.1:8000/?protoco=1&count=1&country=%E5%9B%BD%E5%A4%96 ',
                                timeout=5).json()[0]
        except IndexError:
            raise IPPoolEmpError
    except BaseException :
        print('从IP池获取IP失败，请检查IPProxyPool是否还在运行')
        raise IPProxyPoolRunError


if __name__ == '__main__':
    print(getIP())