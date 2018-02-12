#!/usr/bin/python

#to do:
#get local device ip address for sdp file? Required really?

import socket
import struct
import time

class SDP_Gen():

	def __init__(self, channel, filename): #convert livewire channel number to multicast ip address
		self.channel = channel
		self.filename =filename
		addr = int(self.channel)+0xEFC00000 #Axia channel number + base IP (239.192.0.0 [in hex]) 
		self.multicastaddr = socket.inet_ntoa(struct.pack(">L", addr))

	#heavily borrowed from https://github.com/SythilTech/Python-SDP/blob/master/scripts/sdp.py
	def generate_sdp(self, session_description=""):
	    sdp = ""
	    #Protocol Version ("v=") https://tools.ietf.org/html/rfc4566#section-5.1 (always 0 for us)
	    sdp += "v=0\r\n"
	    #Origin ("o=") https://tools.ietf.org/html/rfc4566#section-5.2
	    username = "bulletins_recorder"
	    sess_id = int(time.time())
	    sess_version = 0
	    nettype = "IN"
	    addrtype = "IP4"
	    sdp += "o=" + username + " " + str(sess_id) + " " + str(sess_version) + " " + nettype + " " + addrtype + " " + self.multicastaddr + "\r\n"
	    #Session Name ("s=") https://tools.ietf.org/html/rfc4566#section-5.3
	    sdp += "s=" + session_description + "\r\n"
	    #Timing ("t=") https://tools.ietf.org/html/rfc4566#section-5.9
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
	    print "writing sdp object to file:{}".format(self.filename)
	    f.write(self.sdp)
	    f = open(self.filename)
	    print ""
	    print f.read()

if __name__ == '__main__':
		livewire_channel = 4263
		sdp_filename = 'source.sdp'
		sdp_object = SDP_Gen(livewire_channel, sdp_filename)
		sdp_object.generate_sdp(session_description='RNZ Bulletin')

