#!/usr/bin/python

#Get properties of audio file using ffprode

import datetime
import time
import ffmpy
import os

test_wav = os.getcwd()+'/test.wav'

class get_properties():

	def __init__(self, audio_file):
		self.input_file = audio_file
		self.string = '-v quiet -show_format -show_streams -pretty -print_format json' #ffprobe input string
		timestamp = ''

	#how to make this return an object describing the audio file properties?
	def properties(self):		#testing for metadata
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} getting metadata of file: {}".format(self.timestamp, self.input_file)
		ff = ffmpy.FFprobe(global_options = '-hide_banner -loglevel warning', inputs = {self.input_file: self.string})
		try:
			ff.run()	
		except Exception as e:
			print "ffprobe error:".format(e)
		finally:
			pass

if __name__ == '__main__':
	try:
		stats = get_properties(test_wav)
		stats.properties()
	except Exception as e:
		print "Error:".format(e)
	finally:
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "Terminated {}.".format(timestamp)
		exit()