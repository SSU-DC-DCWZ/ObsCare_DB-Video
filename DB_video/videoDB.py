import sqlite3
import datetime
import os.path
import errno

class DBvideo:
    def __init__(self, camnum,time):
        self.now = time
        self.dbname = "./DB_video/DB/" + self.now.strftime('%Y%m') + ".db"
        try:  # 파일 경로 생성, DB파일이 존재 하지 않을 경우 DB파일 생성
            if not (os.path.isfile(self.dbname)):
                self.conn = sqlite3.connect(self.dbname)
                self.makedb(camnum)
        except OSError as e:  # 생성 실패 시 오류 코드 출력
            if e.errno != errno.EEXIST:
                print("Dir error")
        raise
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.conn.commit()

    def closedb(self):
        self.conn.close()

    def makedb(self, camnum):
        for i in range(0,camnum):
            self.cur.execute('CREATE TABLE video_' + i + '(id INTEGER, video_address TEXT)')
        self.conn.commit()

    def deldb(self):

    def findrecord(self, findnum):

    def makerecord(self):

    def delrecord(self):

    # def __init__(self, camnum, now):
    #     savename = "./" + now.strftime('%Y%m') + ".db"
    #     try:  # 파일 경로 생성, 경로가 존재 하지 않을 경우 파일 경로 생성
    #         if not (os.path.isdir(savename)):
    #             os.makedirs(os.path.join(savename))
    #     except OSError as e:  # 생성 실패 시 오류 코드 출력
    #         if e.errno != errno.EEXIST:
    #             print("Dir error")
    #     raise
    #
    #     self.conn = sqlite3.connect(savename)
    #     self.cur = self.conn.cursor()
    #     self.cur.execute('CREATE TABLE video_data(day INTEGER, video_address TEXT)')
    #     self.con.close()

    #
    # def adddb(self):
    #     self.cur.execute("INSERT INTO video_data(now.strftime('%d'), './recording/' + str(camnum) + now.strftime('%Y%m%d')")
    #     self.conn.commit()
    #     self.conn.close()
