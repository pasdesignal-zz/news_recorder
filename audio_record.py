#!/usr/bin/python
import ffmpy
import datetime
import os
import threading

#ToDo:
#ignore 255 error for ffmpy terminate

class recorder():
	#is there a bug in the way protocol_whitelist is parsed? Last option always ignored!
	global_options = "-y -hide_banner -protocol_whitelist 'file,udp,rtp,https' -v quiet"
	recstring = "-c:a pcm_s24be -r:a 48000 -ac 2 -t 20:00"
	outstring = "-c:a pcm_s24le"
	audio_input = (os.getcwd()+'/source.sdp')

	def __init__(self, comm, filename):
		self.filename = filename
		if not os.path.isdir(os.path.dirname(self.filename)):
			print "creating wav folder:{}".format(os.path.dirname(self.filename))
			os.makedirs(os.path.dirname(self.filename))
		self.cue = ffmpy.FFmpeg(global_options=self.global_options,inputs={self.audio_input : self.recstring},outputs={self.filename : self.outstring })
		self.comm = comm

	def run(self):
		try:
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} starting recording of file:{}".format(timestamp, self.filename)	
			self.cue.run()
		except ffmpy.FFRuntimeError as e:
				print "ERROR: ffmpeg recording: {}".format(e)

	def terminate(self):
		try:
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} terminating ffmpeg ecording of file:{}".format(timestamp, self.filename)
			self.cue.process.terminate()
		except ffmpy.FFRuntimeError as e:
				print "ERROR: ffmpeg recording: {}".format(e)

	def timeout(self):
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} ERROR: no-one pushed the button or something else went wrong".format(timestamp)
		print "recording timeout occured, forcing end of recording etc"
		self.comm.send('stop_recording')	

if __name__ == '__main__':
	try:
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