#!/usr/bin/python

#Watch a folder and transcode files as they land
#this script requires watchdog module - pip install watchdog

##to do:
#define output formats as setup variables somehow
#housekeeping
#test

from watchdog.events import PatternMatchingEventHandler  
from watchdog.observers import Observer
import os
import datetime
import time
import ffmpy

watch_dir = (os.getcwd()+'/audio/wav/')
transcode_string = ''

class MyHandler(PatternMatchingEventHandler):
	
	patterns = ["*.wav", "*.mp3", "*.ogg"]
	ignore = []
	
	#does the work once called by on_modified
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

	#catches new files and calls process when they have finished landing/growing
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
		ff = ffmpy.FFmpeg(global_options='-y -hide_banner',inputs={wav_in: transcode_string},outputs={wav_out : None })
		print ff.cmd
		ff.run()			

	def housekeeping(self, deleteme):
		print "removing source file:{}".format(deleteme)
		#remove source file after transcode

if __name__ == '__main__':
	try:
	#test folders exists, if not make them!
		if not os.path.exists(watch_dir:
			os.makedirs(watch_dir)
		if not os.path.exists(temp_dir):
			os.makedirs(temp_dir)
		#call and start Observer class
		print "starting watchdog process observing new files..."
		observer = Observer()        #folder watchdog process to monitor wav folder for new files
		observer.schedule(MyHandler(), path=watch_dir)
		observer.start()
		while True:
			print "waiting ..."
			time.sleep(5)
	except Exception as e:
		print "Error:".format(e)
	finally:
		print "outta here..."
		exit()
