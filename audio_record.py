#!/usr/bin/python
import ffmpy
import datetime
import os
import threading

class recorder():
	#is there a bug in the way protocol_whitelist is parsed? Last option always ignored!
	global_options = "-y -hide_banner -protocol_whitelist 'file,udp,rtp,https' -v quiet"
	recstring = "-c:a pcm_s24be -r:a 48000 -ac 2 -t 20:00"
	outstring = "-c:a pcm_s24le"
	audio_input = (os.getcwd()+'/source.sdp')

	def __init__(self, filename):
		self.filename = filename
		self.cue = ffmpy.FFmpeg(global_options=self.global_options,inputs={self.audio_input : self.recstring},outputs={self.filename : self.outstring })

	def run(self):
		try:
			if not os.path.isdir(os.path.dirname(self.filename)):
				print "creating folder:{}".format(os.path.dirname(self.filename))
				os.makedirs(os.path.dirname(self.filename))
			print "starting recording of file:{}".format(self.filename)	
			self.cue.run()
		except Exception as e:
			print "ffmpeg error:{}".format(e)
		finally:
			pass

	def terminate(self):
		try:
			self.cue.process.terminate()
		except Exception as e:
			pass				

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