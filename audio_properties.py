#!/usr/bin/python

#Automatically normalise audio to Amazon Voice Services loudness standard:
#https://developer.amazon.com/docs/flashbriefing/normalizing-the-loudness-of-audio-content.html
#this script requires watchdog module - pip install watchdog
#this script requires ffmpy wrapper module - pip install ffmpy

##to do:
#syslog integration using python syslog library
#add metadata to processed files: processed=yes - where? How to extract metadata and test with existing libraries
#hash the file to identify - dont rely on filename (in case of replace)??? How will this work with replacement file?
# test more!!!

import datetime
import time
import ffmpy

test_wav = os.getcwd()+'/test.wav'

class get_properties():

	def __init__(self, audio_file):
		input_file = audio_file
		string = '-v quiet -show_format -show_streams -pretty -print_format json' #ffprobe input string

	#how to make this return an object describing the audio file properties?
	def properties(self):		#testing for metadata
		self.timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
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
		get_properties(test_wav)
	except Exception as e:
		print "Error:".format(e)
	finally:
		print "Terminated {}.".format(timestamp)
		exit()