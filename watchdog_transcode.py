#!/usr/bin/python

##to do:
#this script requires watchdog module - pip install watchdog

from watchdog.events import PatternMatchingEventHandler  
from watchdog.observers import Observer
import os
import datetime
import time
import ffmpy
import shutil

wav_dir = (os.getcwd()+'/audio/wav/')
temp_dir = (os.getcwd()+'/audio/temp/')
loudnorm_string = '-af loudnorm=I=-14:TP=-3:LRA=11:print_format=json'

class MyHandler(PatternMatchingEventHandler):
	
	patterns = ["*.wav", "*.mp3", "*.ogg"]
	ignore = []
	
	def process(self, event):
		#have we seen this file before?
		if event.src_path not self.ignore:
			self.ignore.append(event.src_path)
			print "processing new file {}".format(event.src_path)
			#print event.src_path, event.event_type         #debug
			#everything here is what happens once the event is triggered
			print "processing file(s) for loudness using FFMPEG..."
			self.temp_file = (temp_dir+(os.path.basename(event.src_path)))
			print "new name:{}".format(self.temp_file)
			self.transcode((event.src_path), self.temp_file)
			self.housekeeping()
		else print "file seen before - no need to process."	

	def on_modified(self, event):
		print "detected new file {}".format(event.src_path)
		#print "modified observer =", observer
		if os.path.exists(event.src_path):
			file_stopped = 0
			while file_stopped == 0:
				size1 = os.path.getsize(event.src_path)
				print "file size:", size1		#debug
				time.sleep(2)
				size2 = os.path.getsize(event.src_path)
				print "file size:", size2		#debug
				if size1 == size2:
					print 'file {} stopped growing...'.format(event.src_path)
					file_stopped = 1	
			if size2 > 0:
				self.process(event)

	def transcode(self, wav_in, wav_out):
		print "initiating ffmpeg transcode process"
		ff = ffmpy.FFmpeg(global_options='-y -hide_banner',inputs={wav_in: None},outputs={wav_out : loudnorm_string })
		print ff.cmd
		ff.run()			

	def housekeeping(self, deleteme):
		print "removing source file:{}".format(deleteme)
		#remove source file after transcode

if __name__ == '__main__':
	try:
	#test folders exists, if not make them!
		if not os.path.exists(wav_dir):
			os.makedirs(wav_dir)
		if not os.path.exists(temp_dir):
			os.makedirs(temp_dir)
		#call and start Observer class
		print "starting watchdog process observing new files..."
		observer = Observer()        #folder watchdog process to monitor wav folder for new files
		observer.schedule(MyHandler(), path=wav_dir)
		observer.start()
		while True:
			print "waiting ..."
			time.sleep(2)
	except Exception as e:
		print "Error:".format(e)
	finally:
		print "outta here..."
		exit()
