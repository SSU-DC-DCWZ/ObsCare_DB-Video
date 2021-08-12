import sqlite3

import cv2
import datetime
import os.path
import errno
from DB_video import videoDB
from DB_log import logDB


class Stream: #cctv 스트리밍을 위한 클래스 설계
    def __init__(self, camnum):
        self.running = True
        self.camnum = camnum    #카메라 번호, cctv 시스템에서는 카메라 위치 번호
        self.sign = 0   #스크린샷이 필요한 상황 발생 시 상황별 번호(0:상황 없음, 1:환자발생, 1~4:도움이 필요한사람)

    def run(self): #스트리밍을 시작하기 위한 함수
        while self.running:
            self.video()
            now = datetime.datetime.now()
            if now.strftime('%H%M%S') == '000000': #일단위 저장을 위해 00시 00분 00초가 되면 스트리밍을 멈추고 재시작
                self.stop()
                self.start()

    def video(self): #영상에 대한 처리를 위함 함수
        ret, frame = self.capture.read()
        showtime = datetime.datetime.now()
        cv2.putText(frame, showtime.strftime('%Y/%m/%d'), (10,470), cv2.FONT_HERSHEY_DUPLEX,0.5,(255,255,255))
        cv2.putText(frame, showtime.strftime('%H:%M:%S'), (555,470), cv2.FONT_HERSHEY_DUPLEX,0.5,(255,255,255))
        cv2.putText(frame, showtime.strftime('CAM' + str(self.camnum+1)), (575,25), cv2.FONT_HERSHEY_DUPLEX,0.7,(255,255,255)) #스트리밍 화면에 시간, 카메라번호 출력
        cv2.imshow(str(self.camnum), frame)
        self.out.write(frame)
        if self.sign >> 0: #상황 발생 시 스크린샷을 위한 처리
            now = datetime.datetime.now()
            name = './data/Situation/' + str(self.sign) + '/' + now.strftime('%Y%m%d%H%M%S_'+str(self.sign)) +'.jpg'
            try:  # 파일 경로 생성, 경로가 존재 하지 않을 경우 파일 경로 생성
                if not (os.path.isdir("./data/Situation/" + str(self.sign))):
                    os.makedirs(os.path.join("./data/Situation/" + str(self.sign)))
            except OSError as e:  # 생성 실패 시 오류 코드 출력
                if e.errno != errno.EEXIST:
                    print("Dir error")
                raise
            cv2.imwrite(name, frame)
            im = logDB.DBlog(self.sign, now, name)
            im.makerecord(self.camnum)
            del im
            self.sign = 0
        # 1ms 동안 키입력 대기 ESC키 눌리면 종료
        if cv2.waitKey(1) == 27:
            self.stop()

    def stop(self): #스트리밍 정지 및 저장, DB에 파일 저장
        self.running = False
        self.capture.release()
        db = videoDB.DBvideo(self.camnum, self.now, self.savename)
        db.makerecord()
        del db

    def start(self): #스트리밍 시작 설정
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