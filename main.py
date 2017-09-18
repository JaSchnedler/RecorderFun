from utils import Recorder, Upload, InputClass, CardReader
import time, os

ssn = None
folder = 'soundfiles/'


def waitforssn():
	global ssn
	print(ssn)
	while ssn is None:
		card = str(CardReader.read()).strip()
		#print("length of card: " + str(len(str(card))))

		if len(str(card)) == 10:
			ssn = card
		else:
			result = InputClass()
			if len(str(result)):
				ssn = result
	print("moving on with ssn: " + ssn)
	return True


def mkdir():
	global folder
	if not os.path.exists(folder):
		os.makedirs(folder)
		print("Created dir: " + folder)


def main():
	global ssn, folder
	runbool = True
	while runbool:
		mkdir()
		print("Program started")
		if waitforssn():
			rec = Recorder(ssn, folder)
			rec.run()
		stop = None
		while stop is None:
			stop = input('Enter something to stop the recording')
			print(' ')
			if str(stop.strip()) == 'stop':
				runbool = False
			time.sleep(0.2)
			print(stop)
		if rec is not None:
			rec.stop()
		filename = ssn
		if os.path.isfile(folder + filename + '.wav'):
			ul = Upload(folder)
			while not ul.upload(filename):
				time.sleep(0.02)
		else:
			print('not working, folder + filename = ' + folder + filename)
		ssn = None
		stop = None

main()
