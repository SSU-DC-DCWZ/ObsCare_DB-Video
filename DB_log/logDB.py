import datetime
import sqlite3
import os


#log 발생에 대한 DB 처리 클래스
class DBlog:
    def __init__(self, situation, time, path): #situation:발생상황
        self.situation = situation
        self.now = time
        self.path = path
        self.connectdb()

    def __del__(self):
        pass

    def connectdb(self): #DB파일 선언 및 테이블 없을 경우 테이블 생성하는 함수
        self.conn = sqlite3.connect('./db/log.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS log_" + str(self.situation) +
                                           " (day INTEGER, camera INTEGER, screenshot_address TEXT)")
        self.conn.commit()

    def closedb(self): #DB 종료 함수
        self.conn.commit()
        self.conn.close()

    def makerecord(self, camnum): #레코드(TIME, PATH)생성 함수
        self.conn.execute("INSERT INTO log_" + str(self.situation) + " VALUES(?,?,?)",
                      (self.now.strftime('%Y%m%d%H%M%S'), camnum, self.path))

        self.conn.commit()
        self.delrecord() # 레코드 생성할 때는 일자가 바뀌었다는 뜻이므로 동시에 레코드 삭제 수행
        self.conn.close()

    def delrecord(self): # 저장기한 만료된 영상에 대한 DB 처리 및 삭제 함수
        lastday = self.now - datetime.timedelta(weeks=10) #저장기한 10주로 설정
        self.cur.execute("SELECT * FROM log_" + str(self.situation) + " WHERE day=" + lastday.strftime('%Y%m%d%H%M%S'))
        try:
            path = self.cur.fetchone()[1]
        except TypeError:  # path가 없을 경우 빈 문자열 반환(상위 레벨에서 비어있을 경우에 해당하는 처리 필요)
            path = ''
        if os.path.isfile(path):
            os.remove(path)
        self.conn.execute("DELETE FROM log_" + str(self.situation) + " WHERE day=" + lastday.strftime('%Y%m%d%H%M%S'))
        self.conn.commit()