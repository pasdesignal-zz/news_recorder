#!/usr/bin/python
#Get properties of audio file using mediainfo
#requires mediainfo: sudo apt install mediainfo
#requires pymediainfo: sudo pip install pymediainfo
import os
import json
import ast
from pymediainfo import MediaInfo

#to do: test for valid file type
# what if the media info fails?

test_wav = os.getcwd()+'/audio/test/test_bulletin.wav'
test_ogg = os.getcwd()+'/audio/test/test_bulletin.ogg'
test_mp3 = os.getcwd()+'/audio/test/test_bulletin.mp3'
test_opus = os.getcwd()+'/audio/test/test_bulletin.opus'

class get_properties():

	def __init__(self, audio_file):  
		self.input = audio_file
		self.duration = 'unknown'
		self.bitdepth = 'unknown'
		self.samplerate = 'unknown'
		self.filesize = 'unknown'
		self.codec = 'unknown'
		self.bitrate = 'unknown'
		self.valid = 0
		if not os.path.exists(self.input):
			print "ERROR: no such file exists"
			exit()
		print "getting metadata of file: {}".format(self.input)
		try:
			media_info = MediaInfo.parse(self.input)
			self.json= json.dumps(media_info.to_data(), indent=2, sort_keys=True)
			#print self.jsonloaded  						#debug
			self.astloaded = ast.literal_eval(self.json)	#no unicode by defualt!
			self.get_codec()
			if self.codec != 'unknown':
				self.get_duration()
				self.get_bitdepth()
				self.get_samplerate()
				self.get_filesize()
				self.get_bitrate()
				self.validate()
		except Exception as e:
			print "MediaInfo error:".format(e)
		finally:
			pass
	
	def get_codec(self):
		self.codec = (self.astloaded['tracks'][0]['codec'])
		if self.codec == 'Wave':
			print ".wav detected"
		elif self.codec == 'MPEG Audio':
			print "mp3 detected"
		elif self.codec == 'OGG':
			print "ogg detected"	
		else:
			print "ERROR: codec test: unknown filetype: {}".format(self.input)

	def get_duration(self):
		if self.codec == 'Wave':
			self.duration = str((self.astloaded['tracks'][0]['duration'])/1000)
		if self.codec == 'MPEG Audio':
			self.duration = str((self.astloaded['tracks'][0]['duration'])/1000)
		if self.codec == 'OGG':
			self.duration = str((self.astloaded['tracks'][0]['duration'])/1000)

	def get_bitdepth(self):
		if self.codec == 'Wave':
			self.bitdepth = str(self.astloaded['tracks'][1]['bit_depth'])	
		if self.codec == 'MPEG Audio':
			pass
		if self.codec == 'OGG':
			pass

	def get_samplerate(self):
		if self.codec == 'Wave':
			self.samplerate = str(self.astloaded['tracks'][1]['other_sampling_rate'][0])
		if self.codec == 'MPEG Audio':
			self.samplerate = str(self.astloaded['tracks'][1]['other_sampling_rate'][0])
		if self.codec == 'OGG':
			self.samplerate = str(self.astloaded['tracks'][1]['other_sampling_rate'][0])

	def get_bitrate(self):
		if self.codec == 'Wave':
			self.bitrate = str((self.astloaded['tracks'][0]['overall_bit_rate']))
		if self.codec == 'MPEG Audio':
			self.bitrate = str((self.astloaded['tracks'][0]['overall_bit_rate']))
		if self.codec == 'OGG':
			self.bitrate = str((self.astloaded['tracks'][0]['overall_bit_rate']))

	def get_filesize(self):
		if self.codec == 'Wave':
			self.filesize = str((self.astloaded['tracks'][0]['file_size']))
		if self.codec == 'MPEG Audio':
			self.filesize = str((self.astloaded['tracks'][0]['file_size']))
		if self.codec == 'OGG':
			self.filesize = str((self.astloaded['tracks'][0]['file_size']))	

	def validate(self):	#this could be fleshed out a bit more to be more sophisticated....
		if self.codec == 'Wave':
			if self.bitdepth == '24' and self.samplerate == '48.0 KHz':
				print ".wav file validation PASSED: {}".format(self.input)
				self.valid = 1
			else:
				print "ERROR: .wav file validation FAILED: {}".format(self.input)
				self.valid = 0

		elif self.codec == 'MPEG Audio':
			if self.bitrate == '64000' and self.samplerate == '48.0 KHz':
				print ".mp3 file validation PASSED: {}".format(self.input)
				self.valid = 1
			else:
				print "ERROR: .mp3 file validation FAILED: {}".format(self.input)
				self.valid = 0
				
		elif self.codec == 'OGG':
			if (self.astloaded['tracks'][1]['other_codec'][0]) == 'Vorbis' and self.samplerate == '48.0 KHz':
				print ".ogg file validation PASSED: {}".format(self.input)
				self.valid = 1
			else:
				print "ERROR: .ogg file validation FAILED: {}".format(self.input)
				self.valid = 0	
		else:
			print "ERROR: validation problem. Filetype not recognised: {}".format(self.input)			

if __name__ == '__main__':
	stats = get_properties(test_wav)
	print "properties of {} :".format(test_wav)
	print "codec", stats.codec
	print "bitdepth", stats.bitdepth
	print "samplerate", stats.samplerate
	print "duration", stats.duration
	print "filesize", stats.filesize
	print "bitrate", stats.bitrate
	print "validate", stats.valid
	stats = get_properties(test_mp3)
	print "properties of {} :".format(test_mp3)
	print "codec", stats.codec
	print "bitdepth", stats.bitdepth
	print "samplerate", stats.samplerate
	print "duration", stats.duration
	print "filesize", stats.filesize
	print "bitrate", stats.bitrate
	print "validate", stats.valid
	stats = get_properties(test_ogg)
	print "properties of {} :".format(test_ogg)
	print "codec", stats.codec
	print "bitdepth", stats.bitdepth
	print "samplerate", stats.samplerate
	print "duration", stats.duration
	print "filesize", stats.filesize
	print "bitrate", stats.bitrate
	print "validate", stats.valid