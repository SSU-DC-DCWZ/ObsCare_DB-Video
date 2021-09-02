import cv2
import datetime
import os.path
import errno
from DB_video import videoDB
from DB_log import logDB

#Stream: cctv 스트리밍을 위한 클래스 설계
class Stream:
    # __int__ : 생성자
    # 파라미터(camnum)
    # camnum: 카메라 번호, PC에 연결된 카메라의 기기 번호
    def __init__(self, camnum):
        self.running = True
        self.camnum = camnum
        # 스크린샷이 필요한 상황 발생 시 상황별 번호(0:상황 없음, 1:환자발생, 1~4:도움이 필요한사람)
        self.sign = 0

    # stop(): 스트리밍 정지 및 저장
    def stop(self):
        self.running = False
        self.capture.release()

    # start() : 스트리밍 시작 설정
    def start(self):
        self.running = True
        # VidoCapture 선언 및 동영상 해상도, 시작시간, 저장경로, 코덱 등 설정
        self.capture = cv2.VideoCapture(self.camnum, cv2.CAP_DSHOW)
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.starttime = datetime.datetime.now()
        self.savename = "./data/Recording/" + str(self.camnum) + "/" + self.starttime.strftime('%Y%m%d') + ".mp4"
        # 파일 경로 생성, 경로가 존재 하지 않을 경우 파일 경로 생성
        try:
            if not (os.path.isdir("./data/Recording/" + str(self.camnum))):
                os.makedirs(os.path.join("./data/Recording/" + str(self.camnum)))
        # 생성 실패 시 오류 코드 출력
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Dir error")
            raise
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.savename, codec, 20.0, ((int(self.width)), (int(self.height))))
        # DB에 동영상 관련 정보 저장
        db = videoDB.DBvideo(self.camnum, self.starttime, self.savename)
        db.makerecord()
        del db
        # 전처리 완료 후 run()호출
        self.run()

    # run() : 스트리밍을 진행하는 함수, 종료코드 받기 전까지 무한 반복
    def run(self): #
        while self.running:
            self.video()
            now = datetime.datetime.now()
            # 일단위 저장을 위해 00시 00분 00초가 되면 스트리밍을 멈추고 저장 후 재시작
            if now.strftime('%H%M%S') == '000000':
                self.stop()
                self.start()

    # video() : 프레임 각각에 대한 처리를 위한 함수
    def video(self):
        ret, frame = self.capture.read()
        showtime = datetime.datetime.now()
        # cctv 화면과 같이 카메라 번호 및 현재 시각 프레임에 입력
        cv2.putText(frame, showtime.strftime('%Y/%m/%d'), (10,470), cv2.FONT_HERSHEY_DUPLEX,0.5,(255,255,255))
        cv2.putText(frame, showtime.strftime('%H:%M:%S'), (555,470), cv2.FONT_HERSHEY_DUPLEX,0.5,(255,255,255))
        cv2.putText(frame, showtime.strftime('CAM' + str(self.camnum+1)), (575,25), cv2.FONT_HERSHEY_DUPLEX,0.7,(255,255,255)) #스트리밍 화면에 시간, 카메라번호 출력
        cv2.imshow(str(self.camnum), frame)
        # 프레임 단위 저장
        self.out.write(frame)
        # 상황 발생 시 스크린샷을 위한 처리
        if self.sign >> 0:
            now = datetime.datetime.now()
            name = './data/Situation/' + str(self.sign) + '/' + now.strftime('%Y%m%d%H%M%S_'+str(self.sign)) +'.jpg'
            # 파일 경로 생성, 경로가 존재 하지 않을 경우 파일 경로 생성
            try:
                if not (os.path.isdir("./data/Situation/" + str(self.sign))):
                    os.makedirs(os.path.join("./data/Situation/" + str(self.sign)))
            # 생성 실패 시 오류 코드 출력
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Dir error")
                raise
            # 스크린샷 수행 및 저장, DB에 해당 정보 추가
            cv2.imwrite(name, frame)
            im = logDB.DBlog(self.sign, now, name)
            im.makerecord(self.camnum)
            del im
            self.sign = 0
        # 1ms 동안 키입력 대기 ESC키 눌리면 종료
        if cv2.waitKey(1) == 27:
            self.stop()