import cv2
import datetime
import os.path
import errno

#cctv 스트리밍을 위한 클래스 설계
class Stream:
    def __init__(self, camnum):
        self.running = False

        self.capture = cv2.VideoCapture(camnum, cv2.CAP_DSHOW)
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        now = datetime.datetime.now()
        savename = "./recording/" + str(camnum) + "/" + now.strftime('%Y%m%d_%H-%M-%S') + ".mp4"
        try:  # 파일 경로 생성, 경로가 존재 하지 않을 경우 파일 경로 생성
            if not (os.path.isdir("./recording/" + str(camnum))):
                os.makedirs(os.path.join("./recording/" + str(camnum)))
        except OSError as e: #생성 실패 시 오류 코드 출력
            if e.errno != errno.EEXIST:
                print("Dir error")
            raise

        codec = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(savename, codec, 20.0, ((int(self.width)), (int(self.height))))

    def run(self):
        while self.running:
            ret, frame = self.capture.read()
            cv2.imshow("VideoFrame1", frame)
            self.out.write(frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                self.stop()

    def stop(self):
        self.running = False
        self.capture.release()

    def start(self):
        self.running = True
        self.run()