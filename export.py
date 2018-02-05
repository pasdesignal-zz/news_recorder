#!/usr/bin/python

import datetime
import os
import time

##TO DO:
#export job via ftp/scp ogg/opus file to ELF(?)

wav_dir = (os.getcwd()+'/audio/wav/')
opus_dir = (os.getcwd()+'/audio/opus/')
sdp_file = (os.getcwd()+'/news_recorder/rnz_national.sdp')
date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = 'rnznews_'+date_time+'.wav'


if __name__ == '__main__':
	try:
		print "starting export task"
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		pass