#!/usr/bin/python

import datetime
import os
import threading
from multiprocessing import Process, Pipe
from sdp_generator import SDP_Gen
from audio_properties import get_properties
from pathfinder_socket import listen_socket
from record import recorder
from audio_trim import silence_trimmer

if __name__ == '__main__':
	try:
		#session variables
		livewire_channel = 4263
		sdp_filename = 'source.sdp'
		bind_interface = '10.212.13.1'
		bind_port=5119
		wav_dir = (os.getcwd()+'/audio/wav/')
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		wav_filename = wav_dir+'rnznews_'+timestamp+'.wav'
		#
		print "\r\n"
		print "{} starting recording job".format(timestamp)
		print "initiating listen socket"
		listen_parent_conn, listen_child_conn = Pipe() 		#Pipes for control of external application processes
		pathfinder = listen_socket(comm=listen_parent_conn, bind=bind_interface, port=bind_port)
		control = Process(target=pathfinder.listen)             
		print "initiating recorder thread"
		sdp_object = SDP_Gen(livewire_channel, sdp_filename)
		sdp_object.generate_sdp(session_description='RNZ Bulletin')
		record_bulletin = record(wav_filename)
		rec_job = threading.Thread(target=recorder.run)
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
				record_bulletin.terminate()
				loop = 0
			else:
				print 'command: {}'.format(command)	
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} closing listen socket".format(timestamp)
		control.terminate()
		print "testing for valid recording..."  #make this a boolean evaluation for valid file
		analyser = get_properties(wav_filename)
		analyser.print_pretty()	
		test_wav = (os.getcwd()+'/audio/test/test_bulletin.wav')
		processed_wav = (os.getcwd()+'/audio/test/processed_bulletin.wav')
		print "opening file:{} for silence trimming".format(test_wav)
		sox_object = silence_trimmer()
		sox_object.trim_start(wav_filename, sox_object.temp)
		print "trimming silence off end of bulletin"
		sox_object.trim_end(sox_object.temp, wav_filename)
		sox_object.housekeeping()
		print "testing for valid recording..."  #make this a boolean evaluation for valid file
		analyser = get_properties(wav_filename)
		analyser.print_pretty()	
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		print "finished"