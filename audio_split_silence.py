#!/usr/bin/python

import sox
import os

#requires sox
#sudo pip install sox

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
		print "trimming silence from start of file..."
		tfm = sox.Transformer()
		tfm.silence(location=1, silence_threshold=0.1, min_silence_duration=0.5, buffer_around_silence=True)
		tfm.build(_input, _output)
		if os.path.isfile(_output):
			print "trim_start success...maybe?"

	def trim_end(self, _input, _output):
		print "trimming silence from end of file..."
		tfm = sox.Transformer()
		tfm.reverse()
		tfm.silence(location=1, silence_threshold=0.1, min_silence_duration=0.5, buffer_around_silence=True)
		tfm.reverse()
		tfm.build(_input, _output)
		if os.path.isfile(_output):
			print "trim end success...maybe?"		

	def get_duration(self, _file):
		self.duration = sox.file_info.duration(_file)

if __name__ == '__main__':
	test_wav = (os.getcwd()+'/audio/test/test_bulletin.wav')
	print "opening file:{}".format(test_wav)
	sox_object = silence_trimmer(test_wav)
	sox_object.get_duration(sox_object.input)
	print "Duration before:{} secs".format(sox_object.duration)
	print "trimming silence off start of bulletin"
	sox_object.trim_start(test_wav, sox_object.temp)
	sox_object.get_duration(sox_object.temp)
	print "Duration after trim_start:{} secs".format(sox_object.duration)
	sox_onject.trim_end(sox_object.temp, test_wav)
	sox_object.get_duration(test_wav)
	print "Duration after trim_end:{} secs".format(sox_object.duration)



		