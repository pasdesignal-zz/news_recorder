#!/usr/bin/python
#requires paramiko:
#sudo pip install paramiko

import paramiko
import os
import sys
#To Do:
# check connectivity to ELF

class check_ssh(): #object to use for duration of bulletin creation

	def __init__(self):
		self.proxy_command = "/usr/bin/ncat --proxy-type http --proxy 172.17.8.1:3128 \%h \%p"
		print self.proxy_command



	def check_it(self, ip, user, key_file, initial_wait=0, interval=0, retries=1):
		ssh = paramiko.SSHClient()
		proxy = paramiko.ProxyCommand(self.proxy_command)
		print "testing SSH connectivity to {} as user {}".format(ip, user)
		ssh.connect(ip, username=user, key_filename=key_file, sock=proxy)
		return True

if __name__ == '__main__':
	try:
		elf_staging = '150.242.42.149'
		elf_user = 'deploy'
		key_file = '/home/deploy/.ssh/id_rsa.pub'
		testconn = check_ssh()
		result = testconn.check_it(elf_staging, elf_user, key_file)
		if result == True:
			print "success bitches!!!"
		else:
			print "failure bitches!!!"	
	except KeyboardInterrupt:
		print "manually interrupted!"
	except Exception as e:
		print "Error:"
		print e
	finally:
		print "finished"