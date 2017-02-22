import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='19941212dD', db='ehproject',charset='utf8')
cur = conn.cursor()  # 光标对象

def writedata(fav,rat,jtitle,language,id):
    if len(jtitle)!=0:
        # 某个在本子标题里插emoji表情的棒子韩化组，我有一句______不知当讲不当讲。
        # 其实怪我没有提前调好数据库编码
        jtitle = jtitle.replace('📤','')
        sql = "update ehdata set Favorited = %s,Ratings = %s,title_jpn = '%s',language = '%s',ex = '1',writed = '1' where id = %s"%(fav,rat,jtitle,language,id)
        try:
            cur.execute(sql)
            print(sql)
        except BaseException:
            print("写入失败，请检查mysql语句")
            print(sql)
            raise
    else:
        sql = 'update ehdata set Favorited = %s,Ratings = %s,language = "%s",ex = "1",writed = "1" where id = %s' % (fav, rat,language,id)
        try:
            print(sql)
            cur.execute(sql)
        except BaseException:
            print("写入失败，请检查mysql语句")
            print(sql)
            raise
    cur.connection.commit()

if __name__ == "__main__":
    writedata(641,14,21,"(サンクリ34) [SAZ (己即是空, soba, 双九朗)] なChuらる★ろりぽっ！！ (魔法少女リリカルなのはA\\')")



