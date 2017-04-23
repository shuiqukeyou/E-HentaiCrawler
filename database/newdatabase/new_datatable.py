# -*- coding: utf-8 -*-
from database.link_database import link_database

FIELD_AND_ATTR = {"id":"int(10) primary key auto_increment","gid":"int(7) not null","token":"varchar(10) not null",
                  "favorited":"int(5)","ratings":"int(5)","archiver_key":"varchar(100)","title":"varchar(500)",
                  "title_jpn":"varchar(500)","elanguage":"varchar(20)","category":"varchar(200)","thumb":"varchar(200)",
                  "uploader":"varchar(100)","posted":"bigint(10)","filecount":"int(5)","filesize":"bigint(10)",
                  "expunged":"varchar(5)","rating":"float(3,2)","torrentcount":"int(2)","tags":"varchar(5000)"}

@link_database
def newtable(cur):
    str=[]
    for field in FIELD_AND_ATTR:
        str.append(field +" " + FIELD_AND_ATTR[field])
    STR = ",".join(str)
    cur.execute('create table ehdata(%s)'% STR)
    print('create table ehdata(%s)'% STR)


if __name__ == "__main__":
    newtable()