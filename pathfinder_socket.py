#!/usr/bin/python

#a listen socket for receiving strings from Pathfinder Server. Uses a pipe to pass messages back from thread to main

#to do:
#make this into a module that can be used  by other scripts
#this needs a lot of wrk - the self.conn attribute is causing headaches.

import time
import socket
from multiprocessing import Process, Pipe
import datetime

class listen_socket():

	def __init__(self, queue, bind, port):
		self.queue = queue
		self.bind = bind
		self.port = int(port)
		self.BUFFER_SIZE = 20  # Normally 1024, but we want fast response -- is this going to be an issue????
		
	def listen(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #attempting to free up the socket from the ole 'TIME-WAIT' state
		s.bind((self.bind, self.port))
		s.listen(1)
		self.conn, self.addr = s.accept()
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print '{} connection received from address:{}'.format(timestamp, self.addr)
		while True:
			data = self.conn.recv(self.BUFFER_SIZE)
			timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
			print "{} received socket data: {}".format(timestamp, data)
			self.queue.put(data)	
			time.sleep(1)

	def close_socket(self):   #this isnt working yet - .conn not an attribute of self?
		print "closing listen socket {}".format(self.port)		
		self.conn.close()

#example of using the pipe and socket
if __name__ == '__main__':
	try:
		listen_port = 5009
		bind_interface = '172.17.2.69'
		print "initiating pipe"
		listen_parent_conn, listen_child_conn = Pipe() 		#Pipes for message bus with socket listen
		print "initiating listen socket"
		pathfinder = listen_socket(comm=listen_parent_conn, bind=bind_interface, port=listen_port)
		control = Process(target=pathfinder.listen)       
		print "starting listen socket on interface {} port: {}".format(bind_interface, listen_port)
		control.start()
		while True:
			command = listen_child_conn.recv()
			if command :
				timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
				print "{} pipe command received: {}".format(timestamp, command)
				if command == 'close_socket':
					print "received close_socket command..."
					break
			time.sleep(1)
		pathfinder.close_socket()
		control.terminate()
	except KeyboardInterrupt:
		print "manually interrupted!"
		pathfinder.close()
		control.terminate()
	except Exception as e:
		print "Error:"
		print e
	finally:
		print "finished"