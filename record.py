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

##TO DO:
#setup cron jobs to call above jobs each hour 1 minute before the hour

wav_dir = (os.getcwd()+'/audio/wav/')
opus_dir = (os.getcwd()+'/audio/opus/')
sdp_file = (os.getcwd()+'/news_recorder/rnz_national.sdp')
date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = wav_dir+'rnznews_'+date_time+'.wav'
#'-c:a pcm_s24be -r:a 48000 -ac 2 -t 30'
#is there a bug in the way protocol_whitelist is parsed? Last option always ignored!
ffmpeg_globals = "-y -hide_banner -protocol_whitelist 'file,udp,rtp,https' -v quiet"
ffmpeg_record_string = "-c:a pcm_s24be -r:a 48000 -ac 2 -t 20:00"

def listen(comm):
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5009
	BUFFER_SIZE = 20  # Normally 1024, but we want fast response
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	conn, addr = s.accept()
	print 'Connection received from address:', addr
	received = 0
	while received == 0:
		data = conn.recv(BUFFER_SIZE)
		print "received data:", data
		received = 1
	print "out now..."
	conn.close()
	comm.send(data)

class record():

	def __init__(self):
		self.cue = ffmpy.FFmpeg(global_options=ffmpeg_globals,inputs={sdp_file : ffmpeg_record_string},outputs={filename : None })

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
		control = Process(target=listen, kwargs={'comm':listen_parent_conn})                     
		print "initiating recorder thread"
		recorder = record()
		rec_job = Process(target=recorder.run())
		print "starting recorder thread"
		rec_job.start()
		print "starting listen socket"
		control.start()
		loop = 1
		while loop == 1:
			command = listen_child_conn.recv()
			print 'command: {}'.format(command)
			if command == 'terminate':
				print "terminating recording process..."
				recorder.terminate()
				loop = 0
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