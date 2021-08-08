import sqlite3

#log 발생에 대한 DB 처리 클래스
class DBlog:
    def __init__(self, situation): #situation:발생상황
        self.situation = situation
        self.connectdb()

    def __del__(self):
        pass

    def connectdb(self): #DB파일 선언 및 테이블 없을 경우 테이블 생성하는 함수
        self.conn = sqlite3.connect('./db/log.db')
        self.cur = self.conn.cursor()
        #카메라 별로 별도의 테이블 생성
        self.cur.execute("CREATE TABLE IF NOT EXISTS log_" + str(self.situation) +
                         " (day INTEGER, camera INTEGER, screenshot_address TEXT, image BLOB )")
        self.conn.commit()

    def closedb(self): #DB 종료 함수
        self.conn.commit()
        self.conn.close()