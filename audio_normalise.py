#!/usr/bin/python
import ffmpy
import os
import shutil
import datetime

#This script takes a .wav file and runs a loudness process on it, creating a file that complies
#with the Amazon Echo audio loudness standards. This requires FFMPEG version with libavfilter that includes 
#the loudnorm module. E.G: FFMPEG 3.4.1
#https://developer.amazon.com/docs/flashbriefing/normalizing-the-loudness-of-audio-content.html

##TO DO:
#validate file (sox?) after loudness processing
#test success
#create two-pass option with argument

class loudness_normaliser():

	def __init__(self):
		self.loudnorm_string = '-map 0:0 -af loudnorm=I=-14:TP=-3:LRA=11:print_format=json -c:a pcm_s24le -ar 48000'
		self.global_string = '-y -hide_banner -loglevel verbose'
		self.temp = (os.getcwd()+'/audio/tmp/temp.wav')
		if os.path.isfile(self.temp):
			print "WARNING: removing existing temp wav file{}".format(self.temp)
			os.remove(self.temp)
		if not os.path.isdir(os.path.dirname(self.temp)):
				print "creating temp folder:{}".format(os.path.dirname(self.temp))
				os.makedirs(os.path.dirname(self.temp))
		
	def normalise(self, _input, _output):
		if not os.path.isfile(_input):
			print "ERROR: no file found: {}".format(_input)
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} initiating ffmpeg loudness processing".format(timestamp)
		self.ff = ffmpy.FFmpeg(global_options=self.global_string, inputs={_input : None},outputs={_output : self.loudnorm_string })
		print self.ff.cmd
		try:
			self.ff.run()
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} ffmpeg loudness processing COMPLETE".format(timestamp)
		except Exception as e:
			print "ERROR: ffmpeg loudness processing: {}".format(e)
		finally:
			pass

	def replace(self, orig_file, new_file):
		if os.path.isfile(new_file): 			#safety checks
			if os.path.isfile(orig_file):  		#safety checks
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
		#test = loudness_normaliser()
		#test.normalise(input_file, test.temp) #process orginal file and save as new file
		#test.replace(input_file, test.temp) #replace orginal file with new file
		loudness_normaliser.normalise(input_file, test.temp) #process orginal file and save as new file
		loudness_normaliser.replace(input_file, test.temp) #replace orginal file with new file
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		pass