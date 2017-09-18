from utils import Recorder, Database, InputClass, CardReader
import time, os

ssn = None
folder = 'soundfiles/'


def ssnreceived():
	global ssn
	print(ssn)
	while ssn is None:
		card = str(CardReader.read()).strip()

		if len(str(card)) == 10:
			ssn = card
		else:
			result = InputClass()
			if len(str(result)):
				ssn = result
		return True
	print("moving on with ssn: " + ssn)
	return False


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
		ssn = None
		print("Program started")
		while not ssnreceived():
			print('waiting for ssn')
		rec = Recorder(ssn,folder)
		rec.run()
		stop = None
		while stop is None:
			stop = input('Enter something to stop the recording')
			print(' ')
			if str(stop.strip()) == 'stop':
				runbool = False
			time.sleep(0.2)
			print(stop)
		print(str(rec))
		if rec is not None:
			rec.stop()
		filename = ssn
		if os.path.isfile(folder + filename):
			db = Database(folder, ssn, filename)
			db.adduser()
			db.addfile()
			db.addfiletouser()

		else:
			print('Not added to database')


main()
