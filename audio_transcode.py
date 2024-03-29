#!/usr/bin/python

#transcode from .wav to .mp3 and .ogg

##to do:
#return pas or fail attribute back to main instead of validation?
#define output formats as setup variables somehow
#can bulletins be 64k?

import os
import datetime
import time
import ffmpy

class transcoder():

	def __init__(self, wav_in):
		self.input = wav_in
		if os.path.exists(self.input):
			self.mp3_string = ('-map 0:0 -ac 1 -b:a 48k \
			-metadata "Album=News Bulletin" \
			-metadata "Track name=Radio New Zealand News" \
			-metadata "Performer=Radio New Zealand" \
			-metadata "Comment=News bulletin recorded at {}"').format(datetime.datetime.now().strftime("%-I%p"))
			self.ogg_string = ('-map 0:0 -ac 1 -b:a 48k \
			-metadata "Album=News Bulletin" \
			-metadata "Track name=Radio New Zealand News" \
			-metadata "Performer=Radio New Zealand" \
			-metadata "Description=News bulletin recorded at {}"').format(datetime.datetime.now().strftime("%-I%p"))
			self.ffmpeg_globals = '-y -hide_banner -v quiet'
		else:
			print "FATAL ERROR: no transcode input file found: {}".format(self.input)

	def transcode_mp3(self, out_filename):
		self.mp3valid = 0
		if not os.path.isdir(os.path.dirname(out_filename)):
			print "creating mp3 folder:{}".format(os.path.dirname(out_filename))
			os.makedirs(os.path.dirname(out_filename))
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} initiating ffmpeg transcode process to mp3".format(timestamp)
		mp3_filename = out_filename
		ff = ffmpy.FFmpeg(global_options=self.ffmpeg_globals, inputs={self.input : None}, outputs={mp3_filename : self.mp3_string})
		print ff.cmd
		try:
			ff.run()
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} COMPLETE: ffmpeg mp3 transcoded file: {}".format(timestamp, mp3_filename)
			self.mp3valid = 1		
		except ffmpy.FFRuntimeError as e:
			print "ERROR: ffmpeg loudness processing: {}".format(e)
		finally:
			pass
	
	def transcode_ogg(self, out_filename):
		self.oggvalid = 0
		if not os.path.isdir(os.path.dirname(out_filename)):
			print "creating ogg folder:{}".format(os.path.dirname(out_filename))
			os.makedirs(os.path.dirname(out_filename))	
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} initiating ffmpeg transcode process to ogg".format(timestamp)
		ogg_filename = out_filename
		ff = ffmpy.FFmpeg(global_options=self.ffmpeg_globals, inputs={self.input : None}, outputs={ogg_filename : self.ogg_string})
		print ff.cmd
		try:
			ff.run()	
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} COMPLETE: ffmpeg mp3 transcoded file: {}".format(timestamp, ogg_filename)
			self.oggvalid = 1
		except ffmpy.FFRuntimeError as e:
			print "ERROR: ffmpeg loudness processing: {}".format(e)
		finally:
			pass

	def housekeeping(self):
		print "removing source file:{}".format(self.input)
		if os.path.exists(self.input):
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} deleting orgiginal recording .wav file: {}".format(timestamp, self.input)
			os.remove(self.input)
			if not os.path.isfile(self.input):
							print "file deleted: {}".format(self.input)
		else:
			print "ERROR: no file found. Cannot delete: {}".format(self.input)					

if __name__ == '__main__':
	try:
		test_wav = (os.getcwd()+'/audio/test/test_bulletin.wav')
		test_mp3 = (os.getcwd()+'/audio/test/test_bulletin.mp3')
		test_ogg = (os.getcwd()+'/audio/test/test_bulletin.ogg')
		t = transcoder(test_wav)
		t.transcode_mp3(test_mp3)
		t.transcode_ogg(test_ogg)
	except Exception as e:
		print "Error:".format(e)
	finally:
		print "outta here..."