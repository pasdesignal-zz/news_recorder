#!/usr/bin/python

import sox
import os

#requires sox
#sudo apt install sox
#sudo apt install libsox-dev
#requires pysox wrapper:
#sudo pip install pysox

#To Do:
#1. get initial file duration
#2. trim silence from start of file
#3. get second duration of file
#4. compare two durations and make sure it is shorter
#5. trin silence from end of file
#6. get third duration of file
#7. compare durations and make sure it is shorter

#sox 20170306-1400-048.mp3 -p silence 1 0.1 0.01% | sox -p output.mp3 reverse silence 1 0.1 0.1% reverse	
#sox original.wav new.wav silence 1 0.5 2% 1 2.0 2% : newfile : restart
#https://github.com/rabitt/pysox
#https://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/

class silence_trimmer():

	def __init__(self, filename):
		self.temp = (os.getcwd()+'/audio/tmp/temp.wav')
		self.input = filename
		self.duration_before = 0
		self.duration_after = 0

	def trim(self):
		#test for existing temp directory and file first
		if os.path.isfile(self.temp):
			print "WARNING: removing existing temp wav file{}".format(self.temp)
			os.remove(self.temp)
		if not os.path.isdir(os.path.dirname(self.temp)):
				print "creating temp folder:{}".format(os.path.dirname(self.temp))
				os.makedirs(os.path.dirname(self.temp))
		print "trimming silence from start of file..."
		sapp = pysox.CSoxApp(self.input, self.temp, effectparams=[('silence', [1, 0.1, '0.01%',]),])
		sapp.flow()

	def duration(self, _file):
		self.duration = sox.file_info.duration(input_filepath)
		print "duration:{}".format(self.duration)

if __name__ == '__main__':
	test_wav = (os.getcwd()+'/audio/test/test_bulletin.wav')
	print "opening file:{}".format(test_wav)
	test = silence_trimmer(test_wav)
	print "Duration before:{}".format(test.duration(test_wav))

		