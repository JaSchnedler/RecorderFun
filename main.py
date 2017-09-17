import threading
from utils import Recorder, Upload, InputClass, CardReader
import time

shouldrecord = True
ssn = None
ul = Upload()

def waitforssn():
	global ssn
	print(ssn)
	while ssn is None:
		card = str(CardReader.read()).strip()
		print("length of card: " + str(len(str(card))))

		if len(str(card)) == 10:
			ssn = card
		else:
			result = InputClass()
			if len(str(result)):
				ssn = result
	print("moving on with ssn: " + ssn)
	return True


def main():
	global ssn
	while True:
		print("Program started")
		if waitforssn():
			thread1 = Recorder((str(ssn)))
			thread1.start()
		stop = None
		while stop is None:
			stop = input('enter something to stop the recording')
			print("you entered: " + str(stop))
			time.sleep(0.2)
			print(stop)

		thread1.stop()
		thread1.join()
		print("thread1 living: " + str(thread1.is_alive()))

		while not ul.upload(ssn):
			time.sleep(0.02)

		ssn = None
		stop = None

		

main()