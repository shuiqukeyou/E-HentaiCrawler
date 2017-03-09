# -*- coding: utf-8 -*-
class dataOV(object):
    def __init__(self, gid = 0,token = '',archiver_key = '',title = '',title_jpn = '',
                  category = '',thumb = '', uploader = '', posted = 0, filecount = 0, filesize = 0,
                 expunged = '', rating = 0, torrentcount = 0, tags = '',favorited = 0, ratings = 0, elanguage = ''):
        self.__gid = gid
        self.__token = token
        self.__favorited = favorited
        self.__ratings = ratings
        self.__archiver_key = archiver_key

        self.__title = title
        self.__title_jpn = title_jpn
        self.__elanguage = elanguage
        self.__category = category
        self.__thumb = thumb

        self.__uploader = uploader
        self.__posted = posted
        self.__filecount  = filecount
        self.__filesize = filesize
        self.__expunged = expunged

        self.__rating = rating
        self.__torrentcount = torrentcount
        self.__tags = tags

        self.__SQL_FIELD = {'gid':self.__gid, 'token':self.__token, "favorited":self.__favorited, "ratings":self.__ratings,"archiver_key":self.__archiver_key,
                            "title":self.__title, "title_jpn":self.__title_jpn,"elanguage":self.__elanguage, "category":self.__category,  "thumb":self.__thumb,
                          "uploader": self.__uploader, "posted":self.__posted, "filecount":self.__filecount, "filesize":self.__filesize, "expunged":self.__expunged,
                          "rating": self.__rating, "torrentcount":self.__torrentcount, "tags":self.__tags}

    def getindex(self):
        return [self.__gid, self.__token]

    def update(self, favorited = 0, ratings = 0, elanguage ='',
               title_jpn = ''):
        self.__SQL_FIELD["favorited"] = favorited
        self.__SQL_FIELD["ratings"] = ratings
        self.__SQL_FIELD["title_jpn"] = title_jpn
        self.__SQL_FIELD["elanguage"] = elanguage

    def __str__(self):
        NUMBER_FIELD = ['gid', 'posted','favcount', 'ratings', 'filecount', 'filesize', 'rating', 'torrentcount',"favorited"]
        datateble = "ehtest"
        attrs = []
        values = []
        for attr in self.__SQL_FIELD:
                attrs.append(attr)
                if attr in NUMBER_FIELD:
                    values.append(str(self.__SQL_FIELD[attr]))
                else:
                    values.append('"' + str(self.__SQL_FIELD[attr]) + '"')
        STR = ","
        attrsstr = STR.join(attrs)
        valuestr = STR.join(values)
        SQL = "insert into %s (%s) values (%s)" % (datateble, attrsstr, valuestr)
        return SQL

    def getSQLStr(self):
        NUMBER_FIELD = ['gid', 'posted','favcount', 'ratings', 'filecount', 'filesize', 'rating', 'torrentcount',"favorited"]
        datateble = "ehtest"
        attrs = []
        values = []
        for attr in self.__SQL_FIELD:
                attrs.append(attr)
                if attr in NUMBER_FIELD:
                    values.append(str(self.__SQL_FIELD[attr]))
                else:
                    values.append('"' + str(self.__SQL_FIELD[attr]) + '"')
        STR = ","
        attrsstr = STR.join(attrs)
        valuestr = STR.join(values)
        SQL = "insert into %s (%s) values (%s)" % (datateble, attrsstr, valuestr)
        return SQL


if __name__ == "__main__" :
    ov = dataOV(gid = 10086, token ='str', archiver_key ='10111', title ='chizaoyaowan', category ='Donjinshi',
                thumb = 'assddd', uploader = 'xx', posted = 123456789, filecount = 50, filesize = 1024000,
                expunged = 'False', rating = 5.0, torrentcount = 2, tags = 'language:N/A')

    data = {'favorited': 3, 'ratings': 7, 'elanguage': 'Thai ', 'title_jpn': '(C91) [GRINP (ねことうふ)] おかしいお姉ちゃん (君の名は。) [タイ翻訳]'}
    ov.update(favorited = data['favorited'], ratings = data['ratings'], elanguage = data['elanguage'], title_jpn = data['title_jpn'])
    print(ov)
