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

	def __init__(self, audio_file):  #to do: test for valid file type
		self.input = audio_file
		if not os.path.exists(self.input):
			print "ERROR: no such file exists"
			exit()
		print "getting metadata of file: {}".format(self.input)
		try:
			media_info = MediaInfo.parse(self.input)
		except Exception as e:
			print "MediaInfo error:".format(e)
		finally:
			self.properties = media_info

	def print_pretty(self):
		print "audio properties of {} :".format(self.input)
		try:
			print json.dumps(self.properties.to_data(), indent=2, sort_keys=True)
		except:
			print("Unexpected error:", sys.exc_info()[0])

if __name__ == '__main__':
	stats = get_properties(test_wav)
	print "properties of {} :".format(test_wav)
	print json.dumps(stats.properties.to_data(), indent=2, sort_keys=True)