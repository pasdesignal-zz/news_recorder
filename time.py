import datetime

def current_bulletin_time():
	timestamp = datetime.datetime.now()
	timestamp_plus = timestamp + datetime.timedelta(minutes=11)
	timestamp_plus = timestamp_plus.replace( minute=00, second=0)
	return timestamp_plus

bulletin_time = current_bulletin_time()
basename = bulletin_time.strftime("%Y%m%d-%H00")+".wav"
print basename