# -*- coding: utf-8 -*-
'''
这个类为获取本子列表的爬虫
传入参数为中断时的页码，如果没有传入，则从第一页开始
如果获取成功，返回结果为一个由本子地址关键字构成的list和上次结果的最后一个值（当ex上有新本子上传时，所有本子的顺序会往后挪动）
如果获取失败，返回结果为这次的页数和上结果的最后一个值，用于重启动爬虫
'''

'''
项目完成后的追记：这个模块几乎是写的最早的，现在回头看简直拿衣服：
单进程、单线程、愚蠢的终止判断、无代理、几乎全靠人力的错误处理、还有一堆BUG（比如两次以上写数据库失败是时，目录爬虫对应的数据库的模块的上一次爬虫位置会为None）
但从这种愚蠢到后面那个（自认为）还算能看的EX绅士爬虫，也算是进步的见证
所以我就不改了（一本正经的偷懒理由）

'''

from bs4 import BeautifulSoup
from time import sleep
from error.error import ExPandaError,ExOpenError
import requests
import re

# 原始cookie
COOKIE_DICK = {'igneous': 'c42418a72', 'ipb_member_id': '3384993', 'ipb_pass_hash': 'f9da27b2b6452259c8c82c9c1bc49889',
               'lv': '1484920972-1485016334'}

EX_COOKIE = requests.utils.cookiejar_from_dict(COOKIE_DICK, cookiejar=None, overwrite=True)


class ex_session(object):
    def __init__(self, page=0):
        self.__page = page  # 当前进行到第几页
        self.__lastindex = None  # 上一页的最后一条
        self.__excookies = requests.utils.cookiejar_from_dict(COOKIE_DICK, cookiejar=None, overwrite=True)

    # 返回结果
    def gethtml(self):
        hlist = self.__read_html()
        if isinstance(hlist, list):
            self.__page += 1
            return hlist
        else:
            print('爬虫出现问题，当前已爬到第%s页，上一页的最后一条是：%s' % (self.__page, self.__lastindex))
            return self.__page

    # 解析获取到的网页
    def __read_html(self):
        self.__hlist = []
        try:
            bsobj = BeautifulSoup(self.__open_next())
            table = bsobj.find('table', {'class': 'itg'})
            # 使用正则表达式获取到当前页所有的
            for link in table.findAll('a', href=re.compile('https://exhentai\.org/g/[0-9]{1,8}/[A-Za-z0-9]{10}/')):
                if 'href' in link.attrs:
                    self.__hlist.append(self.__parse_html(link.attrs['href']))
            self.__lastindex = self.__hlist[-1]
            return self.__hlist
        except TypeError as e:
            print("BeautifulSoup解析失败，请检查你是否被封")
            return None

    # 解析连接为list，用于之后组装JSON
    def __parse_html(self, link):
        return (link.split('/')[4:6])

    # 检查打开ex站的结果
    def __open_next(self):
        try:
            return open_Ex(self.__excookies, 'https://exhentai.org/?page=' + str(self.__page))
        except ExOpenError as se:
            print("也许E绅士服务器大姨妈或者你被ban了")
            self.__html = None
        except ExPandaError as pe:
            print("你获得了一只熊猫或者被封IP的页面，请检查")
            self.__html = None
        except requests.exceptions.SSLError as ssle:
            print("代理服务器未响应，可能是搬瓦工又抽风了，自动等待10秒后重试")
            sleep(10)
            self.__html = None


# 带cookie打开exhentai，如果访问异常，或者吃了熊猫或是被ban了IP，就会抛出错误
def open_Ex(cookie, exurl='https://exhentai.org/'):
    seObj = requests.session()
    ehheaders = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                 'Accept-Encoding': 'gzip, deflate',
                 'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.7, ja; q=0.3',
                 'Connection': 'Keep-Alive',
                 'Host': 'exhentai.org',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}

    ex = seObj.get(exurl, headers=ehheaders, cookies=EX_COOKIE)
    if ex.status_code != 200:
        raise ExOpenError
    elif 'ExHentai.org - The X Makes It Sound Cool' not in ex.text:
        raise ExPandaError
    else:
        return ex.text



if __name__ == "__main__":
    opentest = ex_session()
    opentest.gethtml()
