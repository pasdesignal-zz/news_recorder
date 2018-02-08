#!/usr/bin/python

import json
import threading
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
sdp_file = (os.getcwd()+'/news_recorder/rnz_national.sdp')
filename = wav_dir+'rnznews_'+date_time+'.wav'

class record():

	ffmpeg_globals = "-y -hide_banner -protocol_whitelist 'file,udp,rtp,https' -v quiet"
	ffmpeg_record_string = "-c:a pcm_s24be -r:a 48000 -ac 2 -t 20:00"

	def __init__(self, source, filename):
		self.input = source
		self.filename = filename
		self.cue = ffmpy.FFmpeg(global_options=ffmpeg_globals,inputs={self.input : ffmpeg_record_string},outputs={self.filename : None })

	def run(self):
		try:
			self.cue.run()
		except Exception as e:
			pass

	def terminate(self):
		try:
			self.cue.process.terminate()
		except Exception as e:
			pass				

if __name__ == '__main__':
	try:
		print "initiating listen socket"
		listen_parent_conn, listen_child_conn = Pipe() 		#Pipes for control of external application processes
		pathfinder = listen_socket(comm=listen_parent_conn, bind=bind_interface, port=listen_port)
		control = Process(target=pathfinder.listen)             
		print "initiating recorder thread"
		recorder = record(sdp_file, filename)
		rec_job = Process(target=recorder.run)
		print "starting recorder thread"
		rec_job.start()
		print "starting listen socket on interface {} port: {}".format(bind_interface, listen_port)
		control.start()    
		loop = 1
		while loop == 1:
			command = listen_child_conn.recv()
			print 'command: {}'.format(command)
			if command == 'stop_recording':
				print "terminating recording process..."
				recorder.terminate()
				loop = 0
		control.terminate()
		print "testing for valid recording..."
		stats = get_properties()
		properties = stats.properties(filename) #returns object, use .to_data() method to get dict
		print "properties of {} :".format(filename)
		print json.dumps(properties.to_data(), indent=2, sort_keys=True)		
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		print "finished"