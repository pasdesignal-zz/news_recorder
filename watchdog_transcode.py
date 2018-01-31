
from watchdog.events import PatternMatchingEventHandler  
from watchdog.observers import Observer
import os
import datetime
import time
import ffmpy

wav_dir = '/home/rnzweb/audio/wav/'
loudnorm_string = '-af loudnorm=I=-14:TP=-3:LRA=11:print_format=json'
temp_dir = '/home/rnzweb/audio/temp/'


class MyHandler(PatternMatchingEventHandler):
	patterns = ["*.wav"]

	def process(self, event):
		print "processing file {}".format(event.src_path)
		#print event.src_path, event.event_type         #debug
		#everything here is what happens once the event is triggered
		_files = os.listdir(wav_dir)
		if len(_files) > 0:
			for file in _files:
				print("file detected: {}".format(file))
				print "processing file(s) for loudness using FFMPEG..."
				new_name = (temp_dir+(os.path.basename(event.src_path)))
				print "new name:{}".format(new_name)
				self.normalise(event.src_path, new_name)
			exit()

	def on_modified(self, event):
		print "detected new file {}".format(event.src_path)
		#print "modified observer =", observer
		if os.path.exists(event.src_path):
			file_stopped = 0
			while file_stopped == 0:
				size1 = os.path.getsize(event.src_path)
				print "file size:", size1		#debug
				time.sleep(2)
				size2 = os.path.getsize(event.src_path)
				print "file size:", size2		#debug
				if size1 == size2:
					print 'file {} stopped growing...'.format(event.src_path)
					file_stopped = 1	
			if size2 > 0:
				self.process(event)

	def normalise(self, wav_in, wav_out):
		print "initiating ffmpeg loudness processing"
		ff = ffmpy.FFmpeg(global_options='-v debug',inputs={wav_in: None},outputs={wav_out : loudnorm_string })
		print ff.cmd
		ff.run()			

if __name__ == '__main__':
	#try:
	print "starting watchdog process observing new files..."
	observer = Observer()        #folder watchdog process to monitor wav folder for new files
	observer.schedule(MyHandler(), path=wav_dir)
	observer.start()
	while True:
		print "waiting ..."
		time.sleep(2)
	#except Exception as e:
	#	print "Error:".format(e)
	#finally:
	#	print "outta here..."
	#	exit()
