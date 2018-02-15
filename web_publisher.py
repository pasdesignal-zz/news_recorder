#!/usr/bin/python

#To Do:
# check connectivity to ELF

class check_ssh(): #object to use for duration of bulletin creation

	def __init__(self):
		timestamp = datetime.datetime.now() #get current time
		timestamp_plus = timestamp + datetime.timedelta(minutes=10)	#bring time into next hour because we start early
		self.time = timestamp_plus.replace( minute=00, second=0, microsecond=0) #round down to nearest hour

def check_it(self, ip, user, key_file, initial_wait=0, interval=0, retries=1):
    ssh = paramiko.SSHClient()
	try:
	    ssh.connect(ip, username=user, key_filename=key_file)
	    return True
	except (BadHostKeyException, AuthenticationException, 
	        SSHException, socket.error) as e:
	    print e
	    sleep(interval)

if __name__ == '__main__':
	try:
		elf_staging = '10.128.71.32'
		elf_user = 'deploy'
		key_file = ''
		test = check_ssh()
		test.check_it()
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		print "finished"