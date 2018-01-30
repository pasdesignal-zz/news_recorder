#!/usr/bin/python

from threading import Thread
import ffmpy
import datetime
import os

##TO DO:
#improve logging to file (include ffmpeg stdout and errors)
#folder watchdog process to process wav file - trim to silence (start and between 02:50mins - 03:10mins )
#folder watchdog transcode trimmed .wav file to opus
#folder watchdog process to ftp/scp ogg/opus file to ELF(?)
#setup cron jobs to call above jobs each hour two seconds before the hour
#create test script to test all of above at any moment

wav_dir = '/home/rnzweb/audio/wav/'
opus_dir = '/home/rnzweb/audio/opus/'
sdp_file = '/home/rnzweb/news_recorder/rnz_national.sdp'
date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = 'rnznews_'+date_time+'.wav'
#'-c:a pcm_s24be -r:a 48000 -ac 2 -t 30'
#is there a bug in the way protocol_whitelist is parsed? Last option always ignored!

recorder = ffmpy.FFmpeg(global_options="-v debug -protocol_whitelist 'file,udp,rtp,https'",inputs={sdp_file : '-c:a pcm_s24be -r:a 48000 -ac 2'},outputs={(wav_dir+filename) : None })

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
		rec_job = Thread(target=recorder.run)
		rec_job.start()
		time.sleep(1)
		waiting ...1
		time.sleep(2)
		waiting ...2
		time.sleep(3)
		waiting ...3
		time.sleep(4)
		waiting ...4
		time.sleep(5)
		waiting ...5
		rec_job.process.terminate()
		print "filename:", filename
		#housekeeping()   #this should not be at the start of this script it will slow down start of recording
		record()
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		pass