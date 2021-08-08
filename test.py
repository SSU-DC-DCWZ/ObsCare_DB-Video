from Stream import stream
from DB_video import videoDB
import threading
import datetime

r = stream.Stream(0)
th1 = threading.Thread(target=r.start)
th1.start()
day = datetime.datetime(2021, 8, 8, 00, 00, 00)
d = videoDB.DBvideo(0, day)
a = d.findrecord()
del a
r.sign = 1

