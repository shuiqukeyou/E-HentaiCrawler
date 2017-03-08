#E绅士爬虫项目

早就想干这个了，把E绅士上所有收藏数大于500的同人志筛选出来然后淦TM的撸爆

然而E绅士并没有提供这种功能

所以我就自己做了......也算是练一练手。

由于原代码里有敏感内容：我的常用密码、我的VPS的IP等，所以这个项目彻底跑完后我才将所有代码放上来，结果就是...git的描述乱到爆炸。

#项目依赖

本项目使用的python版本为python3.5，稍微改改应该能做到py2、py3兼容。（说得好像谁会fork这个项目一样）

requests、pymysql、BeautifulSoup4、IPProxyPool。  
注：

* [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)是一个爬取代理IP的爬虫，本项目中的IP池模块基于该项目运行
* IPProxyPool模块另有其自身的依赖，请移步至项目地址查看其所需依赖

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
1. 先准备一个EX绅士的帐号，要求注册时间超过2周

2. 使用database/newdatbase中的new_indextable创建目录表

3. 再运行main中的index_main获取最新的列表，需要EX绅士的cookie。另外这个部分写于过年前，当时我还比较图样。这个模块是单线程、有一堆小BUG、没有代理（会被banIP），所以大概体验极差。另外对应的数据库写入模块请自行做好设定。

4. 运行database/newdatbase中的new_datatable来创建数据表。

5. 运行main中的API_main，比index_main的BUG控制好了点，有了手动更换的代理，仍然是单线程。同样需要修改对应的数据库模块

6. 运行multiprocessing_test中的main函数，用于获取表站的数据，从这里开始需要另外运行IPProxyPool项目。除了IP池耗尽和断网外基本不会崩溃。但是这里是纯多进程，效率低下。同样需要修改数据库模块

7. 运行multiprocessing_thread中的main函数，用于获取里站的数据，需要设定cookie，另外同样需要运行IPProxyPool项目和修改数据库模块。稳定性和性能较多进程版本更强。
___
为了不给E绅士的服务器带来太大负担（毕竟我是白嫖的），哪怕是最后的multiprocessing_thread的爬虫策略也非常保守，嫌慢可以将休眠缩短，进程开多。



##后续
可能会做一个协程版本出来，然后做成长期运行的东西，用来获取E绅士最近三天收藏数最多的日文和中文本，毕竟E绅士的热门功能跟翔一样，一堆western的不要太瞎狗眼。


另外准备对手上的数据做一下简单的数据分析（跟风搞一下大数据，然而48W条数据算什么大数据）

数据分析完毕后可能会共享出来，大家一起淦他娘的撸爆
