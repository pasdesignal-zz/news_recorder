#!/usr/bin/python

import threading
import ffmpy
import datetime
import os
import time
import socket

##TO DO:
#setup cron jobs to call above jobs each hour 1 minute before the hour

wav_dir = (os.getcwd()+'/audio/wav/')
opus_dir = (os.getcwd()+'/audio/opus/')
sdp_file = (os.getcwd()+'/news_recorder/rnz_national.sdp')
date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = 'rnznews_'+date_time+'.wav'
#'-c:a pcm_s24be -r:a 48000 -ac 2 -t 30'
#is there a bug in the way protocol_whitelist is parsed? Last option always ignored!
ffmpeg_globals = "-y -hide_banner -protocol_whitelist 'file,udp,rtp,https' -v warning"
ffmpeg_record_string = "-c:a pcm_s24be -r:a 48000 -ac 2 -t 20:00"

def listen():
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5005
	BUFFER_SIZE = 20  # Normally 1024, but we want fast response
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	conn, addr = s.accept()
	print 'Connection address:', addr
	while 1:
    	data = conn.recv(BUFFER_SIZE)
    	if not data: break
    	print "received data:", data
    	#conn.send(data)  # echo
	conn.close()
	return(data)

recorder = ffmpy.FFmpeg(global_options=ffmpeg_globals,inputs={sdp_file : ffmpeg_record_string},outputs={(wav_dir+filename) : None })

if __name__ == '__main__':
	try:
		print "starting thread 'recorder'"
		rec_job = threading.Thread(target=recorder.run)
		rec_job.daemon = True
		rec_job.start()
		time.sleep(1)
		print "waiting ...1"
		time.sleep(1)
		print "waiting ...2"
		time.sleep(1)
		print "waiting ...3"
		time.sleep(1)
		print "waiting ...4"
		time.sleep(1)
		print "waiting ...5"
		control = listen()
		if control == 'terminate':
			recorder.process.terminate()
		else:
			print "control:{}".format(control)
		#print "filename:", filename
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		pass