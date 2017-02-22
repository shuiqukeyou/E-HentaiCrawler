import random
from time import sleep

from crawler.index import ex_session
from database.write.index import writedata

# 创建数据库和表格
# newtable()

# 创建爬虫对象和数据库读写器
writer = writedata('root','数据库密码','ehproject')
reader = ex_session(15409)

# 初始化变量
lastindex = ['238663', '03b7cf8304']
page = 15409
# 愚蠢的终止判定

endtag = ['9','e56264c60c']
#重试次数
n = 0
k= 0
while(lastindex != endtag):
    templist = reader.gethtml()
    sleep(2+random.uniform(0,2))
    # 重启爬虫
    if isinstance(templist,int):
        print("爬取失败，重试中")
        reader = ex_session(page)
        n +=1
        if n>5:
            print("————————————WARING————————————\n已连续失败超过5次，终止爬虫，请检查网络是否抽风或者IP是否被ban\n————————————WARING————————————")
            break;
    else:
        n = 0
        if lastindex in templist:
            templist = templist[templist.index(lastindex)+1:len(templist)]
        for data in templist:
            writer.write(data)
        print('已爬取完第%s页'%(page))
        lastindex = templist[-1]
        page +=1
    k+=1
    if k == 100:
        sleep(120+random.uniform(0,10))
        k=0




