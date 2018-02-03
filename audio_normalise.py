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

watch_dir = (os.getcwd()+'/audio/wav/')
temp_dir = (os.getcwd()+'/audio/temp/')
input_file = '/home/rnzweb/audio/bulletin_3mins.wav'					#testig only
output_file = '/home/rnzweb/audio/bulletin_3mins_loud_processed.wav'	#testing only
loudnorm_string = '-af loudnorm=I=-14:TP=-3:LRA=11:print_format=json'

def normalise(wav_in, wav_out):
	print "initiating ffmpeg loudness processing"
	ff = ffmpy.FFmpeg(global_options='-y -hide_banner',inputs={wav_in: None},outputs={wav_out : loudnorm_string })
	print ff.cmd
	ff.run()

def replace(orig_file, new_file):
		print "deleting original file:{}".format(orig_file)
		if os.path.isfile(orig_file): 
			os.remove(orig_file)
			if not os.path.isfile(orig_file):
				print "file {} deleted:".format(orig_file)
				print "replacing with processed file:{}".format(new_file)
				shutil.copy(new_file, orig_file)
				if os.path.isfile(orig_file):
					print "file replaced:{}".format(orig_file)
				if os.path.isfile(new_file):
					print "deleting temp file:{}".format(new_file)
					os.remove(new_file)
					if not os.path.isfile(new_file):
						print "file {} deleted".format(self.temp_file)
						print "file operations complete..."
		else:
			print "no file found:{}".format(event.src_path)

if __name__ == '__main__':
	try:
		normalise(input_file, output_file)
		replace(input_file, output_file)
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		pass

