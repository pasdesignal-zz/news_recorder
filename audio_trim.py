#!/usr/bin/python
import sox
import os

#requires sox
#sudo pip install sox
#https://media.readthedocs.org/pdf/pysox/latest/pysox.pdf

#To Do:
#7. compare durations and make sure it is shorter

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
	processed_wav = (os.getcwd()+'/audio/test/processed_bulletin.wav')
	print "opening file:{}".format(test_wav)
	sox_object = silence_trimmer()
	sox_object.get_duration(test_wav)
	time1 = sox_object.duration
	print "Duration before:{} secs".format(time1)
	print "trimming silence off start of bulletin"
	sox_object.trim_start(test_wav, sox_object.temp)
	sox_object.get_duration(sox_object.temp)
	time2 = sox_object.duration
	print "Duration after trim_start:{} secs".format(time2)
	if time2 >= time1:
		print "Nothing trimmed!"
	else:
		print "{} secs removed".format(time1-time2)	
	print "trimming silence off end of bulletin"
	sox_object.trim_end(sox_object.temp, processed_wav)
	sox_object.get_duration(processed_wav)
	time3 = sox_object.duration
	print "Duration after trim_end:{} secs".format(time3)
	if time3 >= time2:
		print "Nothing trimmed!"
	else:
		print "{} secs removed".format(time2-time3)	

		