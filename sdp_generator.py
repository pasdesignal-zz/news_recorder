#!/usr/bin/python
#generate sdp file based on livewire channel number

import socket
import struct
import time

#to do:
#get local device ip address for sdp file? Not really required?
#does this work if no existing sdp file?
#heavily borrowed from https://github.com/SythilTech/Python-SDP/blob/master/scripts/sdp.py

class SDP_Gen():

	def __init__(self, channel, filename): #convert livewire channel number to multicast ip address
		self.filename =filename
		self.channel = channel
		addr = int(self.channel)+0xEFC00000 #Axia channel number + base IP (239.192.0.0 [in hex]) 
		self.multicastaddr = socket.inet_ntoa(struct.pack(">L", addr))
	
	def generate_sdp(self, session_description=""):
	    sdp = ""
	    sdp += "v=0\r\n"
	    username = "bulletins_recorder"
	    sess_id = int(time.time())
	    sess_version = 0
	    nettype = "IN"
	    addrtype = "IP4"
	    sdp += "o=" + username + " " + str(sess_id) + " " + str(sess_version) + " " + nettype + " " + addrtype + " " + self.multicastaddr + "\r\n"
	    sdp += "s=" + session_description + "\r\n"
	    sdp += "t=0 0\r\n"
	    sdp += "a=type:multicast\r\n"
	    #Connection Information ("c=") https://tools.ietf.org/html/rfc4566#section-5.7
	    sdp += "c=" + nettype + " " + addrtype + " " + self.multicastaddr + "\r\n"
	    #Media Descriptions ("m=") https://tools.ietf.org/html/rfc4566#section-5.14
	    sdp += "m=audio " + '5004' + " RTP/AVP"
	    sdp += " " + '96'
	    sdp += "\r\n"
	    sdp += "a=rtpmap:96 L24/48000/2\r\n"
	    self.sdp = sdp	
	    f = open(self.filename, 'w')			
	    print "writing sdp object to file: {}".format(self.filename)
	    f.write(self.sdp)
	    f = open(self.filename)
	    print ""
	    print f.read()

if __name__ == '__main__':
		livewire_channel = 4263
		sdp_filename = 'source.sdp'
		sdp_object = SDP_Gen(livewire_channel, sdp_filename)
		sdp_object.generate_sdp(session_description='RNZ Bulletin')