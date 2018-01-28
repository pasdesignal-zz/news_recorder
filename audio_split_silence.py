#!/usr/bin/python

#To Do:
#Use sox to process .wav file 
#Split .wav file based on silence
#Possible alogithm: 
#1. Split audio based on silence parameters
#2. Test fragemnts for length starting at first fragment
#3. If first fragment > 03:00, append second fragment and test again
#4. Continue until appended fragemtn is very close to 03:00mins in length
#5. save appended .wav file to appropriate folder with appropriate naming for transcode

#sox original.wav new.wav silence 1 0.5 2% 1 2.0 2% : newfile : restart
#https://github.com/rabitt/pysox
#https://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/