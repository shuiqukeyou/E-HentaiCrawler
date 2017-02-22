import pymysql

FIELD=['id','gid','token','Favorited','Ratings','archiver_key','title','title_jpn','language','category','thumb','uploader','posted','filecount','filesize','expunged','rating','torrentcount','tags','ex',"writed"]
ATTR=["int(10) not null primary key auto_increment",'int(7) not null','char(10) not null','int(5)','int(5)','char(100)','varchar(500)','varchar(500)','char(200)','char(200)','char(200)','char(100)','bigint(10)','int(5)','bigint(10)','char(5)','float(3,2)','int(2)','varchar(5000)',"int(1) default '0'","int(1) default '0'"]
# 新建记录数据的数据表
# 字段请参见E绅士wiki上的API部分，在其之上增加了'Favorited'、'Ratings'、'language'、'ex'\'writed'五个字段
# 分别用于记录API无法获取到的收藏数、评分次数、语种，以及标记是否属于ex绅士(默认为0，即不属于EX绅士)、是否已经写入过（默认为0，即没有写入）
def newtable():
    with pymysql.connect(host='127.0.0.1', user='数据库帐号', passwd='数据库密码', db='ehproject') as  conn:
        n = len(FIELD)
        str=[]
        for i in range(n):
            str.append(FIELD[i]+" "+ATTR[i])
        STR = ",".join(str)
        conn.execute('create table ehdata(%s)'% STR)


if __name__ == "__main__":
    newtable()