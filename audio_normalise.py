import ffmpy
import os

#This script takes a .wav file and runs a ludness process on it, creating a file that complies
#with the Amazon Echo audio loudness standards. This requires FFMPEG version with libavfilter that includes 
#the loudnorm module. E.G: FFMPEG 3.4.1
#https://developer.amazon.com/docs/flashbriefing/normalizing-the-loudness-of-audio-content.html

##TO DO:
#make into a module that can be called with args passed to it (input and output file)
#output ffmpeg result and script stdout/stderr to log file
#validate file (sox?) after loudness processing
#test success and then housekeeping

#Amazon reference string
#$ ffmpeg -i test.mp3 -af loudnorm=I=-14:TP=-3:LRA=11:print_format=json -f null -

wav_dir = '/home/rnzweb/audio/wav/'
opus_dir = '/home/rnzweb/audio/opus/'
input_file = '/home/rnzweb/audio/bulletin_3mins.wav'					#testig only
output_file = '/home/rnzweb/audio/bulletin_3mins_loud_processed.wav'	#testing only
loudnorm_string = '-af loudnorm=I=-14:TP=-3:LRA=11:print_format=json'

def normalise(wav_in, wav_out):
	print "initiating ffmpeg loudness processing"
	ff = ffmpy.FFmpeg(global_options='-v debug',inputs={wav_in: None},outputs={wav_out : loudnorm_string })
	print ff.cmd
	ff.run()

#this is copied from other script - needs adapting for this job
def housekeeping():
	print "housekeeping..."
	files_wav= []
	files_wav = os.listdir(wav_dir)
	if len(files_wav) > 0:
		print "removing existing .wav files:", files_wav
		for file in  files_wav:
			try:
				os.remove(wav_dir+file)        
			except OSError:
				pass

if __name__ == '__main__':
	try:
		normalise(input_file, output_file)
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		pass

