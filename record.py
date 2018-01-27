#!/usr/bin/python

import ffmpy
import datetime

##TO DO:
#setup and sync NTP client for VM
#string to name file : name_date+time
#call ffmpeg recrod process and record for 3.30mins
#save to folder location
#folder watchdog process to process wav file - transcode to ogg/opus
#folder watchdog process to ftp/scp ogg/opus file to ELF
#setup cron jobs to call above jobs each hour two seconds before the hour
#log all output to file
#create test script to test all of above at any moment

wav_dir = '/home/rnzweb/audio/wav/'
opus_dir = 'home/rnzweb/audio/opus/'
sdp_file = '/home/rnzweb/news_recorder/rnz_national.sdp'
date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = 'rnznews_'+date_time+'.ogg'

def record():
	ff = ffmpy.FFmpeg(inputs={sdp_file: '-c:a pcm_s24le -r:a 48000 -t 03:30'},outputs={filename: '-c:a libopus -b:a 64k' })
	ff.run()

if __name__ == '__main__':
	record()
