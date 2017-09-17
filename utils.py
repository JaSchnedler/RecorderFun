import pyaudio
import wave
import threading
import ftplib
import random
import time
import os.path


class CardReader:
	@staticmethod
	def read():
		lower = 1000000000
		upper = 9999999999
		time.sleep(3)
		result = random.randint(lower, upper)
		print("random result:" + str(result))
		return result


class Recorder(threading.Thread):

	def __init__(self, name):
		super(Recorder, self).__init__()
		self._stop_event = threading.Event()
		self.CHUNK = 2048
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.RATE = 44100
		self.p = pyaudio.PyAudio()
		self.sound_device_index = 2
		self.SAMPLESIZE = self.p.get_sample_size(self.FORMAT)
		self.frames = []
		self.filename = name
		self.quit = False

	def stop(self):
		print("Stop function called")
		self._stop_event.set()
		self.quit = True

	def run(self):

		for i in range(0,self.p.get_device_count()):
			if 'USB PnP Sound Device' in str(self.p.get_device_info_by_index(i)):
				self.sound_device_index = i

		print("Recording now, filename: " + str(self.filename))
		stream = self.p.open(format=self.FORMAT,
							channels =self.CHANNELS,
							rate=self.RATE,
							input=True,
							input_device_index = self.sound_device_index,
							output=False,
							frames_per_buffer=self.CHUNK)
		while not self.quit:
			data = stream.read(self.CHUNK, False)
			self.frames.append(data)

		stream.stop_stream()
		stream.close()
		print("Frames size: " + str(self.frames.__sizeof__()))
		wf = wave.open(self.filename + ".wav", 'wb')
		print('saved file: ' + self.filename)
		wf.setnchannels(self.CHANNELS)
		wf.setsampwidth(self.SAMPLESIZE)
		wf.setframerate(self.RATE)
		wf.writeframes(b''.join(self.frames))
		wf.close()


class InputClass:
	def __init__(self):
		self.ask()

	def ask(self):
		result = input('Enter your 10 digit ssn')
		self.evaluate(result)

	def evaluate(self, result):
		if len(str(result)) == 10:
			print('You entered: ' + str(result))
			return result
		else:
			print("Your SSN is 10 digits, the first 6 is your birthday DD/MM/YY. Please try again.")
			self.ask()


class Upload:
	def __init__(self):
		self.session = ftplib.FTP('ftp.jacobschnedler.dk', 'jacobschnedler.dk', '4Vreiya8')
		self.session.cwd('pythontesting')

	def upload(self, filename):
		filename = filename +".wav"
		if os.path.isfile(filename):
			file = open(filename, 'rb')
			filename = "stor " + filename  # file to send
			self.session.storbinary(filename, file)  # send the file
			file.close()
			print("uploaded: " + filename)
		self.session.quit()
		return True
