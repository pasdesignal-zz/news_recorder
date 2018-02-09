#!/usr/bin/python

import json
import ffmpy
import datetime
import os
import time
import socket
from multiprocessing import Process, Pipe
from audio_properties import get_properties
from pathfinder_socket import listen_socket

##TO DO:
#setup cron jobs to call above jobs each hour 1 minute before the hour
#is there a bug in the way protocol_whitelist is parsed? Last option always ignored!

wav_dir = (os.getcwd()+'/audio/wav/')
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
filename = wav_dir+'rnznews_'+timestamp+'.wav'

class record():

	global_options = "-y -hide_banner -protocol_whitelist 'file,udp,rtp,https' -v verbose"
	recstring = "-c:a pcm_s24be -r:a 48000 -ac 2 -t 20:00"
	outstring = "-c:a pcm_s24le"
	audio_input = (os.getcwd()+'/rnz_national.sdp')

	def __init__(self, filename):
		self.filename = filename
		self.cue = ffmpy.FFmpeg(global_options=self.global_options,inputs={self.audio_input : self.recstring},outputs={self.filename : self.outstring })

	def run(self):
		try:
			if not os.path.isdir(os.path.dirname(self.filename)):
				print "creating folder:{}".format(os.path.dirname(self.filename))
				os.makedirs(os.path.dirname(self.filename))
			print "starting recording of file:{}".format(self.filename)	
			self.cue.run()
		except Exception as e:
			print "Error", e

	def terminate(self):
		try:
			self.cue.process.terminate()
		except Exception as e:
			pass				

if __name__ == '__main__':
	try:
		print ""
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} starting recording job".format(timestamp)
		print "initiating listen socket"
		listen_parent_conn, listen_child_conn = Pipe() 		#Pipes for control of external application processes
		pathfinder = listen_socket(comm=listen_parent_conn, port=5009)
		control = Process(target=pathfinder.listen)             
		print "initiating recorder thread"
		recorder = record(filename)
		rec_job = Process(target=recorder.run)
		print "starting recorder thread"
		rec_job.start()
		print "starting listen socket on port: {}".format(5009)
		control.start()    
		loop = 1
		while loop == 1:
			command = listen_child_conn.recv()
			print 'command: {}'.format(command)
			if command == 'stop_recording':
				timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
				print "{} terminating recording process".format(timestamp)
				rec_job.terminate()
				#recorder.terminate()
				loop = 0
		control.terminate()
		print "testing for valid recording..."
		analyser = get_properties()
		audio_properties = analyser.properties(filename) #returns object, use .to_data() method to get dict
		print "properties of {} :".format(filename)
		print json.dumps(audio_properties.to_data(), indent=2, sort_keys=True)		
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		print "finished"