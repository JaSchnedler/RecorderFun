import random
import time
import ftplib
import os.path
import os
import signal
import subprocess
from pymongo import MongoClient


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

	def __init__(self, filename, folder):
		self.filename = filename
		self.folder = folder
		self.p = None
		self.condition = True

	def stop(self):
		#if self.p is not None:
			#os.killpg(os.getpgid(self.p.pid), signal.SIGTERM)
		print('Stop function called')
		self.condition = False

	def run(self):
		#record = 'arecord -D hw:1,0 -r 44100 -f S16_LE ' + self.folder + self.filename + '.wav'
		#self.p = subprocess.Popen(record, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
		text_file = open(self.folder + self.filename + '.wav', "w")
		text_file.write('hello world')
		text_file.close()
		time.sleep(1)
		print('wrote hello world')



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


class Database:
	def __init__(self, folder, ssn, filename):
		self.website = 'jacobschnedler.dk'
		self.session = ftplib.FTP('ftp.jacobschnedler.dk', self.website, '4Vreiya8')
		self.session.cwd('pythontesting')
		self.client = MongoClient() # connecting to localhost
		self.db = self.client.recorderdatabase
		self.filecollection = self.db.filecollection
		self.usercollection = self.db.usercollection
		self.folder = folder
		self.ssn = ssn
		self.filename = filename
		self.fileid = ''

	def addfile(self):
		print('adding file url to collection')
		self.filecollection.insert_one({'owner': self.ssn, 'fileurl': self.geturl()})

	def geturl(self):
		url = 'pythontesting' + '.' + self.website + '/' +self.filename
		return url

	def upload(self):
		file = open(self.folder + self.filename + '.wav', 'rb')
		filename = "stor " + self.filename  # file to send
		self.session.storbinary(filename, file)  # send the file
		file.close()
		self.session.quit()

	def adduser(self):
		post = {"ssn": self.ssn}
		self.usercollection.insert_one(post)
		print('added user to collection')

	def addfiletouser(self):
		self.usercollection.update_one({'ssn': self.ssn}, {'$push': {'soundfiles': str(self.geturl())}}, upsert=True)
		print('linked file to user')