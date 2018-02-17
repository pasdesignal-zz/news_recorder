#!/usr/bin/python
#import all the things :)
import datetime
import os
import threading
from multiprocessing import Process, Pipe
from sdp_generator import SDP_Gen
from audio_properties import get_properties
from pathfinder_socket import listen_socket
from audio_record import recorder
from audio_trim import silence_trimmer
from audio_normalise import loudness_normaliser
from xml_generator import xml_machine
from audio_transcode import transcoder

#To Do:
#syslog notification for errors
#test exits are working/elegant
#check for folders before starting? Do this in all modules!!!
#more timestamps!
#reset timeout to larger number! after testing!
#make analyser useful! (loudness stats/test)
#export function
#housekeeping: delete all filetypes generated older than 24 hours: xml, wav, ogg, mp3, temp etc
#make listen socket safer? Will basically parse anything?

class bulletin_object(): 					#basic object to use for duration of bulletin creation

	def __init__(self):
		timestamp = datetime.datetime.now()
		timestamp_plus = timestamp + datetime.timedelta(minutes=10)				#bring time into next hour cause we start early
		self.time = timestamp_plus.replace( minute=00, second=0, microsecond=0) #round down to nearest hour

if __name__ == '__main__':
	try:
		##--SESSION VARIABLES--##
		livewire_channel = 4263 			#4004 for testing #4263 for bulletins (Auckland Livewire)
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
		listen_parent_conn, listen_child_conn = Pipe() 												#Pipe for control of ffmpeg thread
		pathfinder = listen_socket(comm=listen_parent_conn, bind=bind_interface, port=bind_port) 	#pass one end to this listen thread
		bulletin.control = Process(target=pathfinder.listen)             
		print "initiating recorder thread"
		bulletin.record = recorder(comm=listen_parent_conn, filename=bulletin.filepath)
		rec_job = threading.Thread(target=bulletin.record.run)
		print "starting ffmpeg recorder thread"
		rec_job.start()
		print "starting pathfinder listen socket on interface {}, port: {}".format(bind_interface, bind_port)
		bulletin.control.start()   
		t = threading.Timer(1200.0, bulletin.record.timeout)  	#timeout thread in case button never gets pushed! 1200.0 for 20 mins
		t.start()
		loop = 1
		while loop == 1:									
			command = listen_child_conn.recv()
			print 'command: {}'.format(command)
			if command == 'stop_recording':
				t.cancel()										#cancel timeout thread
				timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
				print "{} terminating recording process".format(timestamp)
				bulletin.record.terminate()
				loop = 0
			else:
				print 'command: {}'.format(command)	
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
		bulletin.properties = get_properties(louder.temp)
		if bulletin.properties.valid == 1:
			print "PASSED: .wav valid test OK: {}".format(louder.temp)
			louder.replace(bulletin.filepath, louder.temp) 			#replace orginal file with new file
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
		bulletin.xml.xml_write(os.getcwd()+'/xmls/'+bulletin.time.strftime("%Y%m%d-%H00")+'.xml')
		#test XML here????
		##--EXPORT--##
		#scp file to ELF
		#call ELF script
		##--HOUSEKEEPING--##
		#delete temp and old files >24hours
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		print "finished"