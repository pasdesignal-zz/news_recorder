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

parsed = json.loads(your_json)
>>> print json.dumps(parsed, indent=4, sort_keys=True)
[

if __name__ == '__main__':
	stats = get_properties()
	properties = stats.properties(test_wav)
	parsed = json.loads(properties)
	print "properties of {} :".format(test_wav)
	json.dumps(parsed, indent=4, sort_keys=True)	
	#
	properties = stats.properties(test_ogg)
	parsed = json.loads(properties)
	print "properties of {} :".format(test_ogg)
	json.dumps(parsed, indent=4, sort_keys=True)	
	#
	properties = stats.properties(test_mp3)
	parsed = json.loads(properties)
	print "properties of {} :".format(test_mp3)
	json.dumps(parsed, indent=4, sort_keys=True)
	#
	stats.properties(test_opus)
	parsed = json.loads(properties)
	print "properties of {} :".format(test_opus)
	json.dumps(parsed, indent=4, sort_keys=True)	
