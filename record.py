#!/usr/bin/python

import threading
import ffmpy
import datetime
import os
import time

##TO DO:
#setup cron jobs to call above jobs each hour 1 minute before the hour

wav_dir = (os.getcwd()+'/audio/wav/')
opus_dir = (os.getcwd()+'/audio/opus/')
sdp_file = (os.getcwd()+'/news_recorder/rnz_national.sdp')
date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = 'rnznews_'+date_time+'.wav'
#'-c:a pcm_s24be -r:a 48000 -ac 2 -t 30'
#is there a bug in the way protocol_whitelist is parsed? Last option always ignored!

recorder = ffmpy.FFmpeg(global_options="-y -hide_banner -protocol_whitelist 'file,udp,rtp,https'",inputs={sdp_file : '-c:a pcm_s24be -r:a 48000 -ac 2 -t 20:00'},outputs={(wav_dir+filename) : None })

def housekeeping():
	print "housekeeping..."
	files_wav= []
	files_wav = os.listdir(wav_dir)
	if len(files_wav) > 0:
		print "removing existing .wav files:", files_wav
		for file in  files_wav:
			try:
				os.remove(wav_dir+file)        
			except OSError:
				pass

if __name__ == '__main__':
	try:
		print "starting thread 'recorder'"
		rec_job = threading.Thread(target=recorder.run)
		#rec_job.daemon = True
		rec_job.start()
		time.sleep(1)
		print "waiting ...1"
		time.sleep(2)
		print "waiting ...2"
		time.sleep(3)
		print "waiting ...3"
		time.sleep(4)
		print "waiting ...4"
		time.sleep(5)
		print "waiting ...5"
		recorder.process.terminate()
		#print "filename:", filename
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		pass