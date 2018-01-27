#!/usr/bin/python

import ffmpy
import datetime
import os

##TO DO:
#housekeeping before and after
#folder watchdog process to process wav file - trim to silence (start and between 02:50mins - 03:10mins )
#folder watchdog process trimmed .wav file to opus
#folder watchdog process to ftp/scp ogg/opus file to ELF(?)
#setup cron jobs to call above jobs each hour two seconds before the hour
#log all output to file
#create test script to test all of above at any moment
#try/except clause

wav_dir = '/home/rnzweb/audio/wav/'
opus_dir = '/home/rnzweb/audio/opus/'
sdp_file = '/home/rnzweb/news_recorder/rnz_national.sdp'
date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = 'rnznews_'+date_time+'.wav'

def record():
	print "initiating ffmpeg record of livewire stream"
	ff = ffmpy.FFmpeg(inputs={sdp_file : '-c:a pcm_s24be -r:a 48000 -ac 2 -t 30'},outputs={(wav_dir+filename) : None })
	print ff
	ff.run()

def housekeeping():
	print "housekeeping..."
	files_wav= []
	files_wav = os.listdir(wav_dir)
	if files_wav.len > 0:
		print "removing existing .wav files:", files_xml
		for file in  files_wav:
			try:
				os.remove(wav_dir+file)        
			except OSError:
				pass

if __name__ == '__main__':
	try:
		housekeeping()
		record() 
	except KeyboardInterrupt:
		print "manually interrupted!"
		housekeeping()
	except Exception as e:
		print("Error:%s".format(e))
	finally
		housekeeping()