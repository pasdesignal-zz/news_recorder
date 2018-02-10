#!/usr/bin/python

import socket
import struct
import time


class SDP_Generator():

	def __init__(self, channel):
		self.channel = channel
		#self.multicastAddr = int(self.channel) + 0xEFC00000 #Axia channel number + base IP (239.192.0.0 [in hex]) 
		_addr = int(self.channel)+0xEFC00000
		#print "_addr:", _addr
		#print "hex_addr:", hex(_addr)
		addr_long = int(hex(_addr), 16)
		#print addr_long
		#struct.pack("<L", addr_long)
		self.multicastaddr = socket.inet_ntoa(struct.pack(">L", _addr))
		#print "address:", hex(self.multicastAddr)

	#borrowed from https://github.com/SythilTech/Python-SDP/blob/master/scripts/sdp.py
	def generate_sdp(self, ip, audio_port, rtp_profiles, session_description=" "):
	    sdp = ""
	    #Protocol Version ("v=") https://tools.ietf.org/html/rfc4566#section-5.1 (always 0 for us)
	    sdp += "v=0\r\n"
	    #Origin ("o=") https://tools.ietf.org/html/rfc4566#section-5.2
	    username = "-"
	    sess_id = int(time.time())
	    sess_version = 0
	    nettype = "IN"
	    addrtype = "IP4"
	    sdp += "o=" + username + " " + str(sess_id) + " " + str(sess_version) + " " + nettype + " " + addrtype + " " + ip + "\r\n"
	    #Session Name ("s=") https://tools.ietf.org/html/rfc4566#section-5.3
	    sdp += "s=" + session_description + "\r\n"
	    #Connection Information ("c=") https://tools.ietf.org/html/rfc4566#section-5.7
	    sdp += "c=" + nettype + " " + addrtype + " " + ip + "\r\n"
	    #Timing ("t=") https://tools.ietf.org/html/rfc4566#section-5.9
	    sdp += "t=0 0\r\n"
	    #Media Descriptions ("m=") https://tools.ietf.org/html/rfc4566#section-5.14
	    sdp += "m=audio " + str(audio_port) + " RTP/AVP"
	    for rtp_profile in rtp_profiles:
	        sdp += " " + str(rtp_profile)
	    sdp += "\r\n"
	    sdp += "a=sendrecv\r\n"
	    self.sdp = sdp	

if __name__ == '__main__':
	sdp_object = SDP_Generator(4263)
	print "address:", sdp_object.multicastaddr
	sdp_object.generate_sdp(ip='172.17.2.69', audio_port=5004, rtp_profiles=['test'])
	print ""
	f = open('source.sdp')
	print f.read()
	print""
	print sdp_object.sdp
