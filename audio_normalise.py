#!/usr/bin/python
import ffmpy
import os
import shutil
import datetime
import subprocess
import json
import ast

#This script takes a .wav file and runs a loudness process on it, creating a file that complies
#with the Amazon Echo audio loudness standards. This requires FFMPEG version with libavfilter that includes 
#the loudnorm module. E.G: FFMPEG 3.4.1
#https://developer.amazon.com/docs/flashbriefing/normalizing-the-loudness-of-audio-content.html

##TO DO:
#test success
#make compatibile for opus, mp3 and ogg etc
#what to do if input file not found?

class loudness_normaliser():

	def __init__(self, _input, dual_mode=True):
		self.input = _input			
		if not os.path.isfile(self.input):
			print "ERROR: no file found: {}".format(_input)
			exit()
		self.temp = (os.getcwd()+'/audio/temp/temp.wav')
		if os.path.isfile(self.temp):
			print "WARNING: removing existing temp wav file{}".format(self.temp)
			os.remove(self.temp)
		if not os.path.isdir(os.path.dirname(self.temp)):
				print "creating temp folder:{}".format(os.path.dirname(self.temp))
				os.makedirs(os.path.dirname(self.temp))	
		
		self.first_pass_string = '-map 0:0 -af loudnorm=I=-14:TP=-3:LRA=11:print_format=json -f null -'
		self.loudnorm_string = '-map 0:0 -af loudnorm=I=-14:TP=-3:LRA=11:print_format=json -c:a pcm_s24le -ar 48000'	#only used if dual_mode==False
		self.global_string = '-y -hide_banner -loglevel info'
		if dual_mode == True:			#specify single pass otherwise dual_pass mode by default
			self.first_pass()		
		
	def first_pass(self):
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} initiating ffmpeg loudness first pass measurement".format(timestamp)
		self.ff = ffmpy.FFmpeg(global_options=self.global_string, inputs={self.input : None},outputs={None : self.first_pass_string})
		print self.ff.cmd
		try:
			stdout, stderr = self.ff.run(stderr=subprocess.PIPE)
			self.result = stderr.split("{")[1:]
			self.result = '{%s' % str(self.result[0])
			print "loudness normaliser first pass analysis results:"
			print self.result
			self.json= json.loads(self.result)
			self.input_i = self.json['input_i']
			self.input_tp = self.json['input_tp']
			self.input_lra = self.json['input_lra']
			self.input_thresh = self.json['input_thresh']
			self.offset = self.json['target_offset']
			self.loudnorm_string = ('-af loudnorm=\
				I=-14:TP=-3:LRA=11:measured_I={}:\
				measured_LRA={}:measured_TP={}:\
				measured_thresh={}:offset={}:\
				linear=true:print_format=json \
				-c:a pcm_s24le -ar 48000').format(self.input_i, self.input_lra, self.input_tp, self.input_thresh, self.offset)
			#print self.loudnorm_string	#debug
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} ffmpeg loudnorm first pass complete".format(timestamp)
		except ffmpy.FFRuntimeError as e:
			print "ERROR: ffmpeg loudness processing: {}".format(e)
		finally:
			pass
		
	def normalise(self, _output):
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} initiating ffmpeg loudness processing".format(timestamp)
		self.ff = ffmpy.FFmpeg(global_options=self.global_string, inputs={self.input : None},outputs={_output : self.loudnorm_string })
		print self.ff.cmd
		try:
			self.ff.run()
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} ffmpeg loudness processing COMPLETE".format(timestamp)
		except ffmpy.FFRuntimeError as e:
			print "ERROR: ffmpeg loudness processing: {}".format(e)
		finally:
			pass

	def replace(self, orig_file, new_file): 		#replace these variables with self.input etc
		if os.path.isfile(new_file): 				#safety checks
			if os.path.isfile(orig_file):  			#safety checks
				timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
				print "{} deleting original file:{}".format(timestamp, orig_file)
				os.remove(orig_file)
				if not os.path.isfile(orig_file):
					print "file deleted: {}".format(orig_file)
					print "replacing with processed file: {}".format(new_file)
					shutil.copy(new_file, orig_file)
					if os.path.isfile(orig_file):
						print "file replaced: {}".format(orig_file)
					if os.path.isfile(new_file):
						print "deleting temp file: {}".format(new_file)
						os.remove(new_file)
						if not os.path.isfile(new_file):
							print "file deleted: {}".format(new_file)
							timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
							print " {} file operations complete...".format(timestamp)
			else:
				print "ERROR: no file found:{}".format(orig_fle)
		else:
			print "ERROR: no file found:{}".format(new_file)

if __name__ == '__main__':
	try:
		input_file = (os.getcwd()+'/audio/test/test_bulletin.wav')
		output_file = (os.getcwd()+'/audio/temp/test_bulletin.wav')
		test = loudness_normaliser(input_file)
		test.normalise(output_file) 				#process input file and save as new file
		test.replace(input_file, output_file) 		#replace orginal file with new file
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		pass