
import ffmpy
import os

##TO DO:
#normalise input file and save as new output file

wav_dir = '/home/rnzweb/audio/wav/'
opus_dir = '/home/rnzweb/audio/opus/'
input_file = '/home/rnzweb/audio/bulletin_3mins.wav'
output_file = '/home/rnzweb/audio/bulletin_3mins_loud_processed.wav'
ffmpeg_string = '-af loudnorm=I=-14:TP=-3:LRA=11:print_format=json'

def normalise(wav_in, wav_out):
	print "initiating ffmpeg loudness processing"
	ff = ffmpy.FFmpeg(global_options='-v debug',inputs={wav : ffmpeg_string},outputs={input_file : None })
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

#$ ffmpeg -i test.mp3 -af loudnorm=I=-14:TP=-3:LRA=11:print_format=json -f null -