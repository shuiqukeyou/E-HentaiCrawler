#E绅士爬虫项目

早就想干这个了，把E绅士上所有收藏数大于500的同人志筛选出来然后淦TM的撸爆

然而E绅士并没有提供这种功能

所以我就自己做了...也算是练一练手。

由于原代码里有敏感内容：我的常用密码、我的VPS的IP等，所以这个项目彻底跑完后我才将所有代码放上来，结果就是...git的描述乱到爆炸。  

#项目依赖

本项目使用的python版本为python3.5，因为几个依赖项目都是py2、3兼容的，所以稍微改改应该能做到py2、py3兼容。

使用到的第三方库：requests、pymysql、BeautifulSoup4、IPProxyPool。  

前面三个都是python里很出名的第三方库了，安装方式为：pip install requests pymysql bs4。  
py2和py3共存时请使用pip3 install requests pymysql bs4  
Anaconda选手请用Anaconda的方法安装

关于[IPProxyPool](https://github.com/qiyeboy/IPProxyPool)：

* [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)是一个爬取代理IP的爬虫，本项目中的IP池模块基于该项目运行
* [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)模块另有其自身的依赖，请移步至项目地址查看其所需依赖

#项目介绍

crawler文件夹内为各种爬虫模块：目录爬虫、API爬虫、e绅士表站爬虫、e绅士里站爬虫

database文件夹内为创建、读、写数据表的各模块

ehemail文件夹为一个邮件提醒用模块，作用不大，因为我基本都在电脑旁

error文件夹中存放了一些自定义错误

main文件夹内为目录、API、单线程E绅士表站爬虫的主模块（多进程、多线程不在此文件夹内）

multiprocessing_test文件夹为本子页面的多进程爬虫，爬虫进程仍为单线程IO阻塞，写test是因为当初就随手这么一打

multiprocessing_thread文件夹内为多进程模式的改良版本，调整成了多进程+多线程

###如果谁真要拿去运行的话，运行顺序是这样。
___
1. 先准备一个**EX绅士**的帐号，要求注册时间超过2周

2. 照着网上的各种反熊猫的教程**获取EX绅士的cookie**，并设置config的相关属性

3. **手动运行**database/newdatabase中的newdatabase，创建数据库

4. 运行main模块
___
为了不给E绅士的服务器带来太大负担（毕竟我是白嫖的），请使用尽量保守的爬虫策略，。



##后续
可能会做一个协程版本出来，然后做成长期运行的东西，用来获取E绅士最近三天收藏数最多的日文和中文本，毕竟E绅士的热门功能跟翔一样，一堆western的不要太瞎狗眼。  
（这坑大概是弃了，把新本子的所有种子爬下来，然后做个蜜罐统计每个本子被询问的次数来追踪热门本的效果更好，维护起来也更简单）


另外准备对手上的数据做一下简单的数据分析（跟风搞一下大数据，然而48W条数据算什么大数据）（已完工，当然并那个不算什么大数据）

数据分析完毕后可能会共享出来，大家一起淦他娘的撸爆（已放，其实之前陆续有人找我要过，没公开放链接就是了）  
数据已放出：数据地址：链接: http://pan.baidu.com/s/1boQaILL 密码: 8qsg  并没有更新后面的，所以仍然是截止2月15日

## 更新
2017-4-23 修复BUG，更新说明（macOS上的Queue的qsize()使用不能就毫无办法了）
2017-3-9 修复BUG
2017-3-8 重构代码，现在只需要运行一个main模块就可以开启爬虫
