import ftplib
import random
import time
import os.path
import os
import signal
import subprocess


class CardReader:
	@staticmethod
	def read():
		lower = 1000000000
		upper = 9999999999
		time.sleep(3)
		result = random.randint(lower, upper)
		print('random result: ' + str(result))
		return result


class Recorder():

	def __init__(self, name, folder):
		self.name = name
		self.folder = folder
		self.p = None

	def stop(self):
		if self.p is not None:
			os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)
			print('Stop function called')

	def run(self):
		record = 'arecord -D hw:1,0 -r 44100 -f S16_LE ' + self.folder + self.name + '.wav'
		self.p = subprocess.Popen(record, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)


class InputClass:
	def __init__(self):
		self.ask()

	def ask(self):
		result = input('Enter your 10 digit ssn')
		self.evaluate(result)

	def evaluate(self, result):
		if len(str(result)) == 10:
			#print('You entered: ' + str(result))
			return result
		else:
			print('Your SSN is 10 digits, the first 6 is your birthday DD/MM/YY. Please try again.')
			self.ask()


class Upload:
	def __init__(self, folder):
		self.session = ftplib.FTP('ftp.jacobschnedler.dk', 'jacobschnedler.dk', '4Vreiya8')
		self.session.cwd('pythontesting')
		self.folder = folder


	def upload(self, filename):
		filename = filename + '.wav'
		print('gonna try uploading this file: ' + self.folder + filename)
		try:
			file = open(self.folder + filename, 'rb')
			filename = 'stor ' + filename  # file to send
			self.session.storbinary(filename, file)  # send the file
			file.close()
		except:
			pass
			print('upload failed but moving on')
		print('uploaded: ' + filename)
		self.session.quit()
		return True
