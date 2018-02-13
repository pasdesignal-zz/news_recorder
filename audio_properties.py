#!/usr/bin/python
#Get properties of audio file using mediainfo
#requires mediainfo: sudo apt install mediainfo
#requires pymediainfo: sudo pip install pymediainfo
import os
import json
from pymediainfo import MediaInfo

#to do: test for valid file type
# what if the media info fails?

test_wav = os.getcwd()+'/audio/test/test_bulletin.wav'
#test_ogg = os.getcwd()+'/test.ogg'
#test_mp3 = os.getcwd()+'/test.mp3'
#test_opus = os.getcwd()+'/test.opus'

class get_properties():

	def __init__(self, audio_file):  
		self.input = audio_file
		self.duration = 0
		self.bitdepth = 0
		self.samplerate = 0
		self.codec = None
		if not os.path.exists(self.input):
			print "ERROR: no such file exists"
			exit()
		print "getting metadata of file: {}".format(self.input)
		try:
			media_info = MediaInfo.parse(self.input)
			self.json= json.dumps(media_info.to_data(), indent=2, sort_keys=True)
			#print _json
			self.jsonloaded = json.loads(self.json)
			self.get_duration()
			self.get_bitdepth()
			self.get_samplerate()
			self.get_codec()
		except Exception as e:
			print "MediaInfo error:".format(e)
		finally:
			pass

	def get_duration(self):
		self.duration = (self.jsonloaded['tracks'][1]['other_duration'][3])

	def get_bitdepth(self):
		self.bitdepth = (self.jsonloaded['tracks'][1]['bit_depth'])	

	def get_samplerate(self):
		self.samplerate = (self.jsonloaded['tracks'][1]['other_sampling_rate'])	
	
	def get_codec(self):
		self.codec = (self.jsonloaded['tracks'][0]['codec'])

	def validate(self):
		#first test for file type based on filename or self.codec?
		#various test oncditions
		#if all==1 then pass=1
		pass	#how to do this????

if __name__ == '__main__':
	stats = get_properties(test_wav)
	print "properties of {} :".format(test_wav)
	print stats.json
	print stats.duration