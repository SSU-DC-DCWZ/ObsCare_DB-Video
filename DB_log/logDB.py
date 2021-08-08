import sqlite3

class DBlog:
    def __init__(self, situation):
        self.situation = situation
        self.conn = sqlite3.connect('./db/log.db')
        self.cur = self.conn.cursor()
        self.connectdb()

    def __del__(self):
        pass

    def connectdb(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS log_" + str(self.situation) + "  (day INTEGER, screen_address TEXT, image BLOB )")
        self.conn.commit()