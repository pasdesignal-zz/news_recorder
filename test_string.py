#!/usr/bin/env python

import socket

#send test message to listen socket

TCP_IP = '127.0.0.1
TCP_PORT = 5120
BUFFER_SIZE = 1024
message = 'stop_recording'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print "sending tcp message:{}".format(message)
s.send(message)
s.close()