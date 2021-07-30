import stream
import threading

r = stream.Stream(0)
th = threading.Thread(target=r.start)
th.start()

return test