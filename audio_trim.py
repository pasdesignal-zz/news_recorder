#!/usr/bin/python
import sox
import os

#requires sox
#sudo pip install sox
#https://media.readthedocs.org/pdf/pysox/latest/pysox.pdf

class silence_trimmer():

	def __init__(self):
		self.temp = (os.getcwd()+'/audio/tmp/temp.wav')
		self.duration_before = 0
		self.duration_after = 0
		if os.path.isfile(self.temp):
			print "WARNING: removing existing temp wav file{}".format(self.temp)
			os.remove(self.temp)
		if not os.path.isdir(os.path.dirname(self.temp)):
				print "creating temp folder:{}".format(os.path.dirname(self.temp))
				os.makedirs(os.path.dirname(self.temp))

	def trim_start(self, _input, _output):
		print "trimming silence from start of file: {}".format(_input)
		self.get_duration(_input)
		time1 = self.duration
		tfm = sox.Transformer()
		tfm.silence(location=1, silence_threshold=0.1, min_silence_duration=0.5, buffer_around_silence=True)
		tfm.build(_input, _output)
		if os.path.isfile(_output):
			self.get_duration(_output)
			time2 = self.duration
			if time2 >= time1:
				print "No silence removed"
			else:
				print "{} secs removed".format(time1-time2)
		else:
			print "ERROR: no output file detected"			

	def trim_end(self, _input, _output):
		print "trimming silence from end of file: {}".format(_input)
		self.get_duration(_input)
		time1 = self.duration
		tfm = sox.Transformer()
		tfm.reverse()
		tfm.silence(location=1, silence_threshold=0.1, min_silence_duration=0.5, buffer_around_silence=True)
		tfm.reverse()
		tfm.build(_input, _output)
		if os.path.isfile(_output):
			self.get_duration(_output)
			time2 = self.duration
			if time2 >= time1:
				print "no silence removed"
			else:
				print "{} secs removed".format(time1-time2)
		else:
			print "ERROR: no output file detected"		

	def get_duration(self, _file):
		self.duration = sox.file_info.duration(_file)

	def housekeeping(self):
		if os.path.isfile(self.temp):
			print "removing temp wav file{}".format(self.temp)
			os.remove(self.temp)
			if os.path.isfile(self.temp):
				print "nile removed"
		else:
			print "No file exists:{}".format(self.temp)		

if __name__ == '__main__':
	test_wav = (os.getcwd()+'/audio/test/test_bulletin.wav')
	processed_wav = (os.getcwd()+'/audio/test/processed_bulletin.wav')
	print "opening file:{} for silence trimming".format(test_wav)
	sox_object = silence_trimmer()
	sox_object.trim_start(test_wav, sox_object.temp)
	print "trimming silence off end of bulletin"
	sox_object.trim_end(sox_object.temp, test_wav)
	sox_object.housekeeping()

		