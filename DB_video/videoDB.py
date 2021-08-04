import sqlite3
import datetime
import os.path

class DBvideo:
    def __init__(self, num, time, path): #num=DB 작업할 카메라 번호, time=datetime.datetime.now(), path=동영상의 절대 경로
        self.now = time
        self.camnum = num
        self.path = path
        self.dbname = "./DB_video/DB/" + self.now.strftime('%Y%m') + ".db"
        self.makedb()
        self.cur = self.conn.cursor()
        self.conn.commit()

    def closedb(self):
        self.conn.close()

    def makedb(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur.execute('CREATE TABLE video_' + self.camnum + ' (id INTEGER, video_address TEXT)')
        self.conn.commit()

    def delrecord(self):
        if self.cur.rowcount == 1:
            self.deldb()
        else:
            self.conn.execute('DELETE FROM video_' + self.camnum + ' WHERE id is' + self.now.strftime('%d'))
            self.conn.commit()

    def deldb(self):
        self.closedb()
        if os.path.isfile(self.dbname):
            os.remove(self.dbname)

    def findrecord(self, findnum):
        self.cur.execute('SELECT * FROM viedo_' + findnum + ' WHERE id=' + self.now.strftime('%d'))
        path = self.cur.fetchone()
        return path

    def makerecord(self):
        self.conn.execute('INSERT INTO video_' + self.camnum + ' VALUES (?,?)', self.now.strftime('%d'), self.path)
        self.conn.commit()