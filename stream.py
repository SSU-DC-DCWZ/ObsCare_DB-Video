import cv2
import datetime
import os.path
import errno

class Stream:
    def __init__(self, camnum):
        self.running = False

        self.capture = cv2.VideoCapture(camnum, cv2.CAP_DSHOW)
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        now = datetime.datetime.now()
        savename = "./" + str(camnum) + "/" + now.strftime('%Y%m%d_%H-%M-%S') + ".avi"
        try:  # 파일 경로 생성, 경로가 존재 하지 않을 경우 파일 경로 생성
            if not (os.path.isdir("./" + str(camnum))):
                os.makedirs(os.path.join("./" + str(camnum)))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Dir error")
            raise

        codec = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
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