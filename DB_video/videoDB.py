import sqlite3
from dateutil.relativedelta import *

class DBvideo:
    def __init__(self, num, time, path = None): #num=DB 작업할 카메라 번호, time=datetime.datetime.now(), path=동영상의 절대 경로
        self.now = time
        self.camnum = num
        self.path = path
        if self.path == None:
                self.findtime = time
                self.findnum = num
        self.conn = sqlite3.connect('./db/video.db')
        self.cur = self.conn.cursor()
        self.connectdb()

    def __del__(self):
        pass

    def connectdb(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS video_" + str(self.camnum) + " (day INTEGER, video_address TEXT)")
        self.conn.commit()

    def makerecord(self):
        self.conn.execute("INSERT INTO video_" + str(self.camnum) + " VALUES(?,?)", (self.now.strftime('%Y%m%d'), self.path))
        self.conn.commit()
        self.delrecord()
        self.conn.close()

    def findrecord(self):
        self.cur.execute("SELECT * FROM video_" + str(self.findnum) + " WHERE day=" + self.findtime.strftime('%Y%m%d'))
        try:
            path = self.cur.fetchone()[1]
        except TypeError:
            path = ''
        self.conn.close()
        return path

    def delrecord(self):
        lastday = self.now - relativedelta(months=3)
        self.conn.execute("DELETE FROM video_" + str(self.camnum) + " WHERE day=" + lastday.strftime('%Y%m%d'))
        self.conn.commit()

    def closedb(self):
        self.conn.commit()
        self.conn.close()

