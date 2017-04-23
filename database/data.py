from database.link_database import link_database


timelist = [1174320000,1205942400,1237478400,1269014400,1300550400,1332172800,
            1363708800,1395244800,1426780800,1458403200,1489939200]

comictime = {"c84":1376064000, "c85":1388246400, "c86":1408032000, "c87":1419696000, "c88":1407945600, "c89":1451318400, "c90":1470931200, "c91":1482940800}
# 86400

@link_database
def addart_par(cur):
    cur.execute("select count(*) from ehdata_nonh")
    n =  cur.fetchone()[0]
    i = 1
    while i<=n:
        cur.execute("select tags from ehdata_nonh where id = %s"% i)
        tagstr = cur.fetchone()[0]
        tags = tagstr2tags(tagstr)
        for tag in tags:

            if "artist:" in tag:
                artist = tag.split(":")[1]
                # print("update ehdata_doujinshi set artist = '%s' where id = %s" %(artist, i))
                cur.execute("update ehdata_nonh set artist = '%s' where id = %s" %(artist, i))
                continue
            if "parody:" in tag:
                parody = tag.split(":")[1]
                # print("update ehdata_doujinshi set parody = '%s' where id = %s" %(parody, i))
                cur.execute("update ehdata_nonh set parody = '%s' where id = %s" %(parody, i))
                continue
        i += 1
        cur.connection.commit()

@link_database
def count(cur):
    n = len(timelist)-1
    i = 0
    while i <= n:
        cur.execute('SELECT count(*),sum(favorited),sum(ratings) FROM ehproject.ehdata2 where %s < posted and posted < %s and elanguage = "korean";'% (timelist[i],timelist[i+1]))
        print(cur.fetchone())
        i+=1



@link_database
def comic(cur):
    s = 1174358472
    m = 2592000
    e = 1489049600
    e2 = 1489058435
    l = []
    while s<e2:
        cur.execute('select count(*) from ehproject.ehdata_doujinshi where posted < %s ' % (s+m))
        print(cur.fetchone()[0])
        s = s+m


@link_database
def kanc(cur):
    s = 1371254492
    e = 1489040799
    m = 2592000
    while s<e:
        l = []
        cur.execute('select count(*),sum(Favorited),sum(ratings) from ehproject.ehdata_doujinshi where %s < posted and posted < %s and parody = "touhou project" and elanguage = "japanese" and filecount < 100' % (s,s+m))
        sql = cur.fetchone()
        for data in sql:
            str = data.__str__()
            str = str.replace("Decimal('","")
            str = str.replace("Decimal('", "')")
            if str == 'None':
                str = 0;
            l.append(str)
        print(l)
        s = s+m

@link_database
def touc(cur):
    s = 1176009438
    e = 1489038172
    m = 2592000
    while s<e:
        l = []
        cur.execute('select count(*),sum(Favorited),sum(ratings) from ehproject.ehdata_doujinshi where %s < posted and posted < %s and parody = "touhou project" and filecount < 100' % (s,s+m))
        sql = cur.fetchone()
        for data in sql:
            str = data.__str__()
            str = str.replace("Decimal('","")
            str = str.replace("Decimal('", "')")
            if str == 'None':
                str = 0;
            l.append(str)
        print(l)
        s = s+m

def tagstr2tags(str):
    str = str.replace("[","")
    str = str.replace("]", "")
    str = str.replace("'", "")
    strs = str.split(",")
    return strs



if __name__ == '__main__':
    pass
