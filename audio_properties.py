#!/usr/bin/python

#Get properties of audio file using mediainfo
#requires mediainfo: sudo apt install mediainfo
#requires pymediainfo: sudo pip install pymediainfo


import os
import json
from pymediainfo import MediaInfo

test_wav = os.getcwd()+'/test.wav'
test_ogg = os.getcwd()+'/test.ogg'
test_mp3 = os.getcwd()+'/test.mp3'
test_opus = os.getcwd()+'/test.opus'

class get_properties():

	def __init__(self):
		self.input = ''
	#how to make this return an object describing the audio file properties?
	#test for valid file types
	def properties(self, audio_file):
		self.input = audio_file
		print "getting metadata of file: {}".format(self.input)
		try:
			media_info = MediaInfo.parse(self.input)
		except Exception as e:
			print "ffprobe error:".format(e)
		finally:
			return media_info

if __name__ == '__main__':
	stats = get_properties()
	properties = stats.properties(test_wav) #returns object, use .to_data() method to get dict
	print "properties of {} :".format(test_wav)
	print json.dumps(properties.to_data(), indent=2, sort_keys=True)
	#
	properties = stats.properties(test_ogg)
	print "properties of {} :".format(test_ogg)
	print json.dumps(properties.to_data(), indent=2, sort_keys=True)
	#
	properties = stats.properties(test_mp3)
	print "properties of {} :".format(test_mp3)
	print json.dumps(properties.to_data(), indent=2, sort_keys=True)
	#
	properties = stats.properties(test_opus)
	print "properties of {} :".format(test_opus)
	print json.dumps(properties.to_data(), indent=2, sort_keys=True)
