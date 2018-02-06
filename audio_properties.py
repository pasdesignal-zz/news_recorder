#!/usr/bin/python

#Get properties of audio file using ffprode

import ffmpy
import os

test_wav = os.getcwd()+'/test.wav'
test_ogg = os.getcwd()+'/test.ogg'
test_mp3 = os.getcwd()+'/test.mp3'
test_opus = os.getcwd()+'/test.opus'

class get_properties():

	def __init__(self):
		self.input = ''
		self.string = '-v quiet -show_format -show_streams -pretty -print_format json' #ffprobe input string

	#how to make this return an object describing the audio file properties?
	def properties(self, audio_file):		#testing for metadata
		self.input = audio_file
		print "getting metadata of file: {}".format(self.input)
		ff = ffmpy.FFprobe(global_options = '-hide_banner -loglevel warning', inputs = {self.input: self.string})
		try:
			ff.run()	
		except Exception as e:
			print "ffprobe error:".format(e)
		finally:
			pass

if __name__ == '__main__':
	stats = get_properties()
	stats.properties(test_wav)
	stats.properties(test_ogg)
	stats.properties(test_mp3)
	stats.properties(test_opus)