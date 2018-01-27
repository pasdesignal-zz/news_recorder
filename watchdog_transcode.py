
from watchdog.events import PatternMatchingEventHandler  
from watchdog.observers import Observer
import os
import datetime

wav_dir = '/home/rnzweb/audio/wav/'
opus_dir = '/home/rnzweb/audio/opus/'
sdp_file = '/home/rnzweb/news_recorder/rnz_national.sdp'
date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = 'rnznews_'+date_time+'.wav'

class MyHandler(PatternMatchingEventHandler):
	
	patterns = ["*.wav"]

##This needs to be improved to tolerate empty/bad xmls...
	def process(self, event):
		print event.src_path, event.event_type         #debug
		#everything here is what happens once the event is triggered
		_files = os.listdir(event.src_path)
		if len(_files) > 0:
			for file in _files:
				print("file detected:%s", format(file))
			exit()

	def on_modified(self, event):
		print "modified observer =", observer
		print event.src_path
		if os.path.exists(event.src_path):
			file_stopped = 0
			while file_stopped == 0:
				size1 = os.path.getsize(event.src_path)
				print "File size:", size1		#debug
				time.sleep(0.5)
				size2 = os.path.getsize(event.src_path)
				print "File size:", size2		#debug
				if size1 == size2:
					file_stopped = 1
			if size2 > 0:
				self.process(event)

if __name__ == '__main__':
	try:
		print "starting watchdog process observing new files in folder:", wav_dir
		observer = Observer()        #folder watchdog process to monitor wav folder for new files
		observer.schedule(MyHandler(), path=wav_dir)
		wav_files =[]
		wav_files = os.listdir(wav_dir)
		count = len(wav_files)
		while len(wav_files) == count:
			time.sleep(1)
			wav_files = os.listdir(wav_dir)
			print "no new files bro..."
	except Exception as e:
		print("Error:%s".format(e))
	finally:
		print "outta here..."
		exit()
