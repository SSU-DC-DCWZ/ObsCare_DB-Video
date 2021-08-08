import cv2
import datetime
import os.path
import errno
from DB_video import videoDB

class Stream: #cctv 스트리밍을 위한 클래스 설계
    def __init__(self, camnum):
        self.running = True
        self.camnum = camnum
        self.sign = 0

    def run(self):
        print("start")
        while self.running:
            self.video()
            now = datetime.datetime.now()
            if now.strftime('%H%M%S') == '000000':
                self.stop()
                self.start()

    def video(self):
        ret, frame = self.capture.read()
        cv2.imshow("VideoFrame1", frame)
        self.out.write(frame)
        k = cv2.waitKey(1)
        if self.sign >> 0:
            print("screenshot")
            now = datetime.datetime.now()
            name = './data/Situation/' + str(self.sign) + '/' + now.strftime('%Y%m%d_%H_%M_%S') +'.jpg'
            try:  # 파일 경로 생성, 경로가 존재 하지 않을 경우 파일 경로 생성
                if not (os.path.isdir("./data/Situation/" + str(self.sign))):
                    os.makedirs(os.path.join("./data/Situation/" + str(self.sign)))
            except OSError as e:  # 생성 실패 시 오류 코드 출력
                if e.errno != errno.EEXIST:
                    print("Dir error")
                raise
            cv2.imwrite(name, frame)
            self.sign = 0

        if k == 27:
            self.stop()


    def stop(self):
        self.running = False
        self.capture.release()
        DB = videoDB.DBvideo(self.camnum, self.now, self.savename)
        DB.makerecord()

    def start(self):
        self.running = True
        self.capture = cv2.VideoCapture(self.camnum, cv2.CAP_DSHOW)
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.now = datetime.datetime.now()
        self.savename = "./data/Recording/" + str(self.camnum) + "/" + self.now.strftime('%Y%m%d') + ".mp4"
        try:  # 파일 경로 생성, 경로가 존재 하지 않을 경우 파일 경로 생성
            if not (os.path.isdir("./data/Recording/" + str(self.camnum))):
                os.makedirs(os.path.join("./data/Recording/" + str(self.camnum)))
        except OSError as e:  # 생성 실패 시 오류 코드 출력
            if e.errno != errno.EEXIST:
                print("Dir error")
            raise
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.savename, codec, 20.0, ((int(self.width)), (int(self.height))))
        self.run()