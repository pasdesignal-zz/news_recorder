#!/usr/bin/python

#Watch a folder and transcode files as they land
#this script requires watchdog module - pip install watchdog

##to do:
#define output formats as setup variables somehow
#housekeeping
#test

import os
import datetime
import time
import ffmpy

test_wav = (os.getcwd()+'/audio/test/test_bulletin.wav')
test_mp3 = (os.getcwd()+'/audio/test/test_bulletin.mp3')
test_ogg = (os.getcwd()+'/audio/test/test_bulletin.ogg')

class transcoder():

	def __init__(self, wav_in):
		self.input = wav_in
		self.mp3_string = '-map 0:0'
		self.ogg_string = '-map 0:0'
		self.ffmpeg_globals = '-y -hide_banner'

	def transcode_mp3(self, out_filename):
		if os.path.exists(self.input):
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} initiating ffmpeg transcode process to mp3".format(timestamp)
			mp3_filename = out_filename
			ff = ffmpy.FFmpeg(global_options=self.ffmpeg_globals, inputs={self.input : None}, outputs={mp3_filename : self.mp3_string})
			print ff.cmd
			ff.run()
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} COMPLETE: ffmpeg mp3 transcoded file: {}".format(timestamp, mp3_filename)		
		else:
			print "ERROR: no file found: {}".format(self.wav_in)

	def transcode_ogg(self, out_filename):
		if os.path.exists(self.input):
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} initiating ffmpeg transcode process to ogg".format(timestamp)
			ogg_filename = out_filename
			ff = ffmpy.FFmpeg(global_options=self.ffmpeg_globals, inputs={self.input : None}, outputs={ogg_filename : self.ogg_string})
			print ff.cmd
			ff.run()	
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} COMPLETE: ffmpeg mp3 transcoded file: {}".format(timestamp, ogg_filename)			
		else:
			print "ERROR: no file found: {}".format(self.wav_in)		

	#is this necessary?
	def housekeeping(self, deleteme):
		print "removing source file:{}".format(deleteme)
		#remove source file after transcode

if __name__ == '__main__':
	try:
		t = transcoder(test_wav)
		t.transcode_mp3(test_mp3)
		t.transcode_ogg(test_ogg)
	except Exception as e:
		print "Error:".format(e)
	finally:
		print "outta here..."
