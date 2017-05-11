import threading
import time
def printer(message):
	for i in range(10):
		print message
		time.sleep(1)
t = threading.Thread(target=printer,args=("thread",))
t.start()
threading._Thread_