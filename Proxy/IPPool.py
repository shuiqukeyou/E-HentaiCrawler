import requests
import json
from time import sleep
from error.error import ProxyInvaError,IPPoolEmpError,IPProxyPoolRunError,BanIPError
URL = 'http://e-hentai.org/api.php'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch, br',
          'Accept-Language': 'zh-CN,zh;q=0.8',
          'Connection': 'keep-alive',
          'DNT': '1',
          'Host': 'e-hentai.org',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

TEST_JSON_STR = {'method': 'gdata', 'gidlist': [[186384, '8ee236ef21']], 'namespace': 1}
TEST_JSON = json.dumps(TEST_JSON_STR).encode("utf-8")
'''
三个结果：1.返回一个IPandport，2.抛出IP池已空错误，3.抛出IPProxyPool运行错误
'''

# 基于IPProxyPool项目运行，IPProxyPool是一个爬取代理的爬虫，项目地址：https://github.com/qiyeboy/IPProxyPool

def getIP():
    testCount = 0
    while True:# 循环到给出一个IP或者抛出错误为止
        try:
            IPandport = getip_from_pool()
            ip = testIP(IPandport)
            testCount = 0
            delIP(ip)
            ip = ip[0:2]
            return ip
        except ProxyInvaError as e:# 如果IP不可用，最多测试三次，三次如果都是失败则舍弃该IP，并重置计数器
            print('5秒后重新进行测试')
            sleep(5)
            testCount += 1
            if testCount >=3:
                print('已重复测试五次，删除该IP')
                delIP(IPandport)
                testCount = 0
        except BanIPError:
            print('删除该IP')
            delIP(IPandport)



# 删除一个已经被ban或者已经失效的一个IP
def delIP(ip):
    try:
        # 如果成功删除或者不成功删除（那个IP被IPProxyPool的自动检测给干掉了之类的），都意味着那个IP不在了
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
        r = requests.post(URL,headers=headers,proxies=proxies ,data=TEST_JSON,timeout = 5)# 组装请求
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
        return requests.get('http://127.0.0.1:8000/?types=0&protoco=2&count=1&country=%E5%9B%BD%E5%A4%96 ',
                            timeout = 5).json()[0]
    except IndexError:
        try:
            return requests.get('http://127.0.0.1:8000/?types=1&protoco=2&count=1&country=%E5%9B%BD%E5%A4%96 ',
                                timeout=5).json()[0]
        except IndexError:
            try:
                return requests.get('http://127.0.0.1:8000/?type=0protoco=1&count=1&country=%E5%9B%BD%E5%A4%96 ', timeout=5).json()[0]
            except IndexError:
                try:
                    return requests.get('http://127.0.0.1:8000/?type=1protoco=1&count=1&country=%E5%9B%BD%E5%A4%96 ', timeout=5).json()[0]
                except IndexError:
                    raise IPPoolEmpError
    except BaseException :
        print('从IP池获取IP失败，请检查IPProxyPool是否还在运行')
        raise IPProxyPoolRunError


if __name__ == '__main__':
    print(getIP())