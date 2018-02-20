#!/usr/bin/python
#import all the things :)
import datetime
import time
import os
import threading
import argparse
from multiprocessing import Process
from multiprocessing.queues import SimpleQueue
from sdp_generator import SDP_Gen
from audio_properties import get_properties
from pathfinder_socket import listen_socket
from audio_record import recorder
from audio_trim import silence_trimmer
from audio_normalise import loudness_normaliser
from xml_generator import xml_machine
from audio_transcode import transcoder

#To Do:
#fix terminate loop BS
#better way to timeout kill
#syslog notification for errors
#test exits are working/elegant
#more timestamps!
#make analyser useful! (loudness stats/test)
#export function
#housekeeping: delete all filetypes generated older than 24 hours: xml, wav, ogg, mp3, temp etc
#make listen socket safer? Will basically parse anything?

parser = argparse.ArgumentParser(description='Record a news bulletin and publish. Use --test for testing.', epilog='')
parser.add_argument('--test', action='store_true', default=False, help='Test mode. Use for testing purposes only. Uses alternative livewire channel and local socket')
arguments = parser.parse_args()

class bulletin_object(): 					#basic object to use for duration of bulletin creation

	def __init__(self):
		timestamp = datetime.datetime.now()
		timestamp_plus = timestamp + datetime.timedelta(minutes=10)				#bring time into next hour cause we start early
		self.time = timestamp_plus.replace( minute=00, second=0, microsecond=0) #round down to nearest hour	

	def housekeeping(self):
		print "housekeeping..."
		#delete old files
		
if __name__ == '__main__':
	try:
		##--SESSION VARIABLES--##
		livewire_channel = 4263		#4004 for testing #4263 for bulletins (Auckland Livewire)
		sdp_filename = 'source.sdp'
		bind_interface = '10.212.13.1'		#for socket strings from Pathfinder
		bind_port=5119						#for socket strings from Pathfinder
		wav_dir = (os.getcwd()+'/audio/wav/')
		mp3_dir = (os.getcwd()+'/audio/mp3/')
		ogg_dir = (os.getcwd()+'/audio/ogg/')
		#test for folders here
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		template_xml = (os.getcwd()+'/diginews_template.xml')
		podcast_baseurl = 'http://podcast.radionz.co.nz/news/'
		if arguments.test == True:
			print "Test argument used. Setting up alternative session variables..."
			livewire_channel = 4004 		#no silence
			bind_interface = '127.0.0.1'		#for socket strings from test script
			bind_port=5120		
		##--RECORD--##
		print "\r\n"
		print "{} starting bulletin recording job...".format(timestamp)
		bulletin = bulletin_object()
		bulletin.xml = xml_machine()
		bulletin.xml.parse_template(template_xml)
		bulletin.xml.broadcast_at = bulletin.time.strftime("%Y-%m-%d %H:00")
		bulletin.xml.archive_at = (bulletin.time+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:00")	#plus 1 day
		bulletin.filepath = wav_dir+bulletin.time.strftime("%Y%m%d-%H00")+".wav"
		bulletin.mp3_filepath = mp3_dir+bulletin.time.strftime("%Y%m%d-%H00")+".mp3"
		bulletin.ogg_filepath = ogg_dir+bulletin.time.strftime("%Y%m%d-%H00")+".ogg"
		bulletin.xml.mp3_url = podcast_baseurl+bulletin.time.strftime("%Y%m%d-%H00")+"-048.mp3"
		bulletin.xml.ogg_url = podcast_baseurl+bulletin.time.strftime("%Y%m%d-%H00")+"-00.ogg"
		bulletin.sdp = SDP_Gen(livewire_channel, sdp_filename)
		bulletin.sdp.generate_sdp(session_description='RNZ Bulletin')
		print "initiating listen socket"
		listen_queue = SimpleQueue() 												#Pipe for control of ffmpeg thread
		pathfinder = listen_socket(queue=listen_queue, bind=bind_interface, port=bind_port) 	#pass one end to this listen thread
		bulletin.control = Process(target=pathfinder.listen)             
		print "starting pathfinder listen socket on interface {}, port: {}".format(bind_interface, bind_port)
		bulletin.control.start()  
		print "initiating recorder thread"
		rec_job = Process(target=recorder, args=(bulletin.filepath,))
		print "starting ffmpeg recorder thread"
		rec_job.start()
		time.sleep(1)
		while rec_job.is_alive():
			print "ffmpeg recording alive:", rec_job.is_alive()
			if not listen_queue.empty():							
				command = listen_queue.get()
				print 'command received: {}'.format(command)
				if command == 'stop_recording':
					timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
					print "{} terminating recording process".format(timestamp)
					break
				else:
					print 'command: {}'.format(command)	
			time.sleep(5)		
		rec_job.terminate()
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} closing listen socket".format(timestamp)
		bulletin.control.terminate()
		##--VALIDATE--##
		print "testing for valid recording..."
		bulletin.properties = get_properties(bulletin.filepath)
		if bulletin.properties.valid == 1:
			print "PASSED: .wav valid test OK: {}".format(bulletin.filepath)
		else:
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} FATAL ERROR: invalid .wav file detected. Cannot continue: {}".format(timestamp, bulletin.filepath)
			exit()
		##--REMOVE SILENCE--##
		print "opening file:{} for silence trimming".format(bulletin.filepath)
		sox_object = silence_trimmer()
		sox_object.trim_start(bulletin.filepath, sox_object.temp)
		print "trimming silence off end of bulletin"
		sox_object.trim_end(sox_object.temp, bulletin.filepath)
		sox_object.housekeeping()
		##--VALIDATE--##
		print "testing for valid audio file after silence trimming..."
		bulletin.properties = get_properties(bulletin.filepath)
		if bulletin.properties.valid == 1:
			print "PASSED: .wav valid test OK: {}".format(bulletin.filepath)
		else:
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} FATAL ERROR: invalid .wav file detected. Cannot continue: {}".format(timestamp, bulletin.filepath)
			exit()
		bulletin.xml.duration = bulletin.properties.duration		#add audio duration to xml	
		##--NORMALISE LOUDNESS--##
		louder = loudness_normaliser(bulletin.filepath)
		louder.normalise(louder.temp) 								#process orginal file and save as new file
		##--VALIDATE--##
		print "testing for valid audio file after loudness process..."
		bulletin.properties = get_properties(bulletin.filepath)
		if bulletin.properties.valid == 1:
			print "PASSED: .wav valid test OK: {}".format(bulletin.filepath)
		else:
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} FATAL ERROR: invalid .wav file detected. Cannot continue: {}".format(timestamp, louder.temp)
			exit()
		##--TRANSCODE--##
		bulletin.transcoder = transcoder(bulletin.filepath)
		bulletin.transcoder.transcode_mp3(bulletin.mp3_filepath)
		bulletin.transcoder.transcode_ogg(bulletin.ogg_filepath)
		##--VALIDATE MP3--##										#should this be folded into module?
		#print "testing for valid mp3 audio file after transcode..."
		#bulletin.mp3valid =bulletin.properties.valid
		if bulletin.transcoder.mp3valid == 1:
			print "PASSED: mp3 valid test OK: {}".format(bulletin.mp3_filepath)
			bulletin.properties = get_properties(bulletin.mp3_filepath)
			bulletin.xml.mp3_size = bulletin.properties.filesize
		else:
			print "ERROR: mp3 valid test BAD: {}".format(bulletin.mp3_filepath)
			#what to do here? Exit?
		##--VALIDATE OGG--##
		#print "testing for valid ogg audio file after transcode..."
		#bulletin.oggvalid =bulletin.properties.valid
		if bulletin.transcoder.oggvalid == 1:
			print "PASSED: ogg valid test OK: {}".format(bulletin.ogg_filepath)
			bulletin.properties = get_properties(bulletin.ogg_filepath)
			bulletin.xml.ogg_size = bulletin.properties.filesize
		else:
			print "ERROR: ogg valid test BAD: {}".format(bulletin.ogg_filepath)
		if bulletin.transcoder.mp3valid == 1 and bulletin.transcoder.oggvalid == 1:
			bulletin.transcoder.housekeeping()
		else:
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} FATAL ERROR: bad transcoded files detected. Exiting.".format(timestamp)
			exit()
		##--GENERATE XML--##
		xml_filename = (os.getcwd()+'/xmls/'+bulletin.time.strftime("%Y%m%d-%H00")+'.xml')
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} generating XML for ingest to ELF: {}".format(timestamp, xml_filename)
		bulletin.xml.xml_write(xml_filename)
		#test XML here????
		##--EXPORT--##
		#scp file to ELF
		#call ELF script
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		bulletin.housekeeping()
		print "finished"