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

#To Do:
#name files correctly according to existing workflows
#remove old bulletin recordings (greater than 24 hours?)
#make analyser useful! (boolean test for valid file, get duration and return as attribute, safe for multiple file types, loudness stats/test)
#create XML for ELF
#export function

class bulletin_object():

	def __init__(self):
		self.basename = ''

def current_bulletin_time():
	timestamp = datetime.datetime.now()
	timestamp_plus = timestamp + datetime.timedelta(minutes=10)	#bring time into next hour because we start early
	timestamp_plus = timestamp_plus.replace( minute=00, second=0, microsecond=0).strftime("%Y%m%d-%H00") #round down to nearest hour
	return timestamp_plus

if __name__ == '__main__':
	try:
		##--SESSION VARIABLES--##
		livewire_channel = 4263
		sdp_filename = 'source.sdp'
		bind_interface = '10.212.13.1'
		bind_port=5119
		wav_dir = (os.getcwd()+'/audio/wav/')
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		template_xml = (os.getcwd()+'/diginews_template.xml')
		##--RECORD--##
		print "\r\n"
		print "{} starting recording job".format(timestamp)
		bulletin = bulletin_object()
		bulletin.xml = xml_machine()
		bulletin.xml.parse_template(template_xml)
		bulletin.time = current_bulletin_time()
		bulletin.xml.broadcast_at = bulletin.time
		bulletin.basename = bulletin.time+".wav"
		bulletin.filepath = wav_dir+bulletin.basename
		print "initiating listen socket"
		listen_parent_conn, listen_child_conn = Pipe() 		#Pipes for control of external application processes
		pathfinder = listen_socket(comm=listen_parent_conn, bind=bind_interface, port=bind_port)
		control = Process(target=pathfinder.listen)             
		print "initiating recorder thread"
		sdp_object = SDP_Gen(livewire_channel, sdp_filename)
		sdp_object.generate_sdp(session_description='RNZ Bulletin')
		bulletin.record = recorder(bulletin.filepath)
		rec_job = threading.Thread(target=bulletin.record.run)
		print "starting ffmpeg recorder thread"
		rec_job.start()
		print "starting pathfinder listen socket on interface {}, port: {}".format(bind_interface, bind_port)
		control.start()    
		loop = 1
		while loop == 1:
			command = listen_child_conn.recv()
			print 'command: {}'.format(command)
			if command == 'stop_recording':
				timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
				print "{} terminating recording process".format(timestamp)
				bulletin.record.terminate()
				loop = 0
			else:
				print 'command: {}'.format(command)	
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} closing listen socket".format(timestamp)
		control.terminate()
		##--VALIDATE--##
		print "testing for valid recording..."  #make this a boolean evaluation for valid file, not sure how yet!
		###***validity test here***
		##--REMOVE SILENCE--##
		print "opening file:{} for silence trimming".format(bulletin.filepath)
		sox_object = silence_trimmer()
		sox_object.trim_start(bulletin.filepath, sox_object.temp)
		print "trimming silence off end of bulletin"
		sox_object.trim_end(sox_object.temp, bulletin.filepath)
		sox_object.housekeeping()
		bulletin.properties = get_properties(bulletin.filepath)
		print "duration: {}".format(bulletin.properties.duration)
		bulletin.xml.duration = bulletin.properties.duration	#add duration to xml
		##--VALIDATE--##
		print "testing for valid recording..."  #make this a boolean evaluation for valid file
		##--NORMALISE LOUDNESS--##
		louder = loudness_normaliser()
		louder.normalise(bulletin.filepath, louder.temp) #process orginal file and save as new file
		louder.replace(bulletin.filepath, louder.temp) #replace orginal file with new file
		##--VALIDATE--##
		##--TRANSCODE--##
		###***get mp3_url and mp3_size here and add to xml
		##***get ogg_url and ogg_size here and add to xml
		##--VALIDATE--##
		##--GENERATE XML--##
		bulletin.xml.xml_write((os.getcwd()+'/elf-test.xml'))
		##--EXPORT--##
		##--HOUSEKEEPING--##
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		print "finished"