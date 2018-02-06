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

from watchdog.events import PatternMatchingEventHandler  
from watchdog.observers import Observer
import os
import datetime
import time
import ffmpy
import shutil
import argparse

#command line arguments
parser = argparse.ArgumentParser(description='Automatically detect new audio files and apply loudness processing according to AVS defined standards...', epilog='')
parser.add_argument('--test', action='store_true', default=False, help='Test mode. Use for testing purposes only. Sets up and uses local folders for watchdog process: ../audio/wav and ../audio/temp')
arguments = parser.parse_args()

#ffmpeg "loudnorm" filter settings string
loudnorm_string = '-map 0:0 -af loudnorm=I=-14:TP=-3:LRA=11:print_format=json -b:a 192k -ar 44100'
#loudnorm_string = '-map 0:0 -af loudnorm=I=-14:TP=-3:LRA=11:print_format=json -b:a 192k -ar 44100 -metadata Genre=Processed'
#ffmpeg input string
input_string = ''
ffmpeg_global_settings ='-y -hide_banner -loglevel warning' 
#ffprobe input string
stats_string = '-v quiet -show_format -show_streams -pretty -print_format json'

class MyHandler(PatternMatchingEventHandler):	#this is the observer class, triggers "process" method when "on_modified" method sees file changes
	patterns = ["*.mp3", "*.ogg"]				#file whitelist - will ignore all other files except those listed
	ignore = []
	timestamp = ''
	
	def process(self, event):					#only called when files modified in watch directory
		print "processing file {} for loudness normalisation using FFMPEG...".format(event.src_path)
		self.temp_file = (temp_dir+(os.path.basename(event.src_path)))
		print "temp file name:{}".format(self.temp_file)
		#self.properties((event.src_path))		#testing for metadata
		self.normalise((event.src_path), self.temp_file)
		#self.properties((event.src_path))		#testing for metadata
		self.replace(event.src_path, self.temp_file)

	def on_modified(self, event):
		if event.src_path not in self.ignore:	#have we seen this file before?
			self.ignore.append(event.src_path)
			self.timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} detected new file {}".format(self.timestamp, event.src_path)
			if os.path.exists(event.src_path):
				file_stopped = 0
				while file_stopped == 0:
					size1 = os.path.getsize(event.src_path)
					#print "file size:", size1		#debug
					time.sleep(6)
					size2 = os.path.getsize(event.src_path)
					#print "file size:", size2		#debug
					if size1 == size2:
						print 'file {} stopped growing...'.format(event.src_path)
						file_stopped = 1	
				if size2 > 0:
					self.process(event)
		else:
			pass	

	def properties(self, wav_in):		#testing for metadata
		self.timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} getting metadata of file: {}".format(self.timestamp, wav_in)
		ff = ffmpy.FFprobe(global_options = '-hide_banner -loglevel warning', inputs = {wav_in: stats_string})
		try:
			ff.run()			
		except Exception as e:
			print "ffprobe error:".format(e)
		finally:
			pass
	
	def normalise(self, wav_in, wav_out): 	#use ffmpeg "loudnorm" filter to apply AVS loudness standards to audio files
		self.timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} initiating ffmpeg loudness processing".format(self.timestamp)
		ff = ffmpy.FFmpeg(global_options = ffmpeg_global_settings, inputs = {wav_in: None}, outputs = {wav_out : loudnorm_string })
		try:
			ff.run()			
		except Exception as e:
			print "ffmpeg error:".format(e)
		finally:
			self.timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} loudness normalisation complete".format(self.timestamp)
	
	def replace(self, orig_file, new_file):		#replace roginal file with processed file safely (wrap this in try/except workflow)
		print "deleting original file:{}".format(orig_file)
		try:
			if os.path.isfile(orig_file): 
				os.remove(orig_file)
				if not os.path.isfile(orig_file):
					print "file {} deleted:".format(orig_file)
					print "replacing with processed file:{}".format(new_file)
					shutil.copy(new_file, orig_file)
					if os.path.isfile(orig_file):
						print "file replaced:{}".format(orig_file)
					if os.path.isfile(new_file):
						print "deleting temp file:{}".format(new_file)
						os.remove(new_file)
						if not os.path.isfile(new_file):
							print "file {} deleted".format(self.temp_file)
							
			else:
				print "no file found:{}".format(orig_file)
		except Exception as e:
			print "file operation error:".format(e)
		finally:
			self.timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} file operations complete...".format(self.timestamp)

if __name__ == '__main__':
	try:
		#directories
		watch_dir = '/audio-store/diginews/'
		temp_dir = '/home/rnzweb/audio_normaliser/audio/temp/'
		if arguments.test == True:
			print 'Command line argument "--test" (test mode): %s' % arguments.test
			watch_dir = (os.getcwd()+'/audio/wav/')		
			temp_dir = (os.getcwd()+'/audio/temp/')
		#test folders exists, if not create them
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} starting watchdog_normalise process".format(timestamp)
		if not os.path.exists(watch_dir):
			if arguments.test == True:
				os.makedirs(watch_dir)				#used for testing only
			else:
				print "WARNING: no audio directory found:{}, exiting".format(watch_dir)
				exit()
		if not os.path.exists(temp_dir):
			print "no temp directory found:{}, creating".format(temp_dir)
			os.makedirs(temp_dir)
		observer = Observer()        				#folder watchdog process to monitor wav folder for new files
		observer.schedule(MyHandler(), path=watch_dir)
		observer.start()
		print "waiting for new files in folder:{}".format(watch_dir)
		while True:
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} awaiting new files to process...".format(timestamp)
			time.sleep(600)
	except Exception as e:
		print "Error:".format(e)
	finally:
		print "Terminated {}.".format(timestamp)
		exit()