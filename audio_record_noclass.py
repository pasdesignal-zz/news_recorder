#!/usr/bin/python
import ffmpy
import datetime
import os

#ToDo:
#ignore 255 error for ffmpy terminate

def recorder(filename):
	#is there a bug in the way protocol_whitelist is parsed? Last option always ignored!
	filename = filename
	global_options = "-y -hide_banner -protocol_whitelist 'file,udp,rtp,https' -v quiet"
	recstring = "-c:a pcm_s24be -r:a 48000 -ac 2 -t 20:0"
	outstring = "-c:a pcm_s24le"
	audio_input = (os.getcwd()+'/source.sdp')
	if not os.path.isdir(os.path.dirname(filename)):
		print "creating wav folder:{}".format(os.path.dirname(filename))
		os.makedirs(os.path.dirname(filename))
	cue = ffmpy.FFmpeg(global_options=global_options,inputs={audio_input : recstring},outputs={filename : outstring })
	timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
	print "{} starting recording of file:{}".format(timestamp, filename)	
	cue.run()
	print "finished recording...."

if __name__ == '__main__':
	try:
		import threading
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		wav_filename = wav_dir+'rnznews_'+timestamp+'.wav'
		print ""
		record_me = recorder(wav_filename)
		rec_job = threading.Thread(target=record_me.run)
		print "starting ffmpeg recorder thread"
		rec_job.start()
		print "testing for valid recording..."
		analyser = get_properties(wav_filename)
		analyser.print_pretty()	
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		print "finished"