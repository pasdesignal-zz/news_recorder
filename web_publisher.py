#!/usr/bin/python
#requires paramiko:
#sudo pip install paramiko

import paramiko
import os
import sys
#To Do:
# check connectivity to ELF

class check_ssh(): #object to use for duration of bulletin creation

	def __init__(self, sock):
		self.sock = sock

	def check_it(self, ip, user, key_file, initial_wait=0, interval=0, retries=1):
		ssh = paramiko.SSHClient()
		print "testing SSH connectivity to {} as user {}".format(ip, user)
		ssh.connect(ip, username=user, key_filename=key_file, sock=self.sock)
		return True

if __name__ == '__main__':
	elf_staging = '150.242.42.149'
	elf_user = 'deploy'
	key_file = '/home/deploy/.ssh/id_rsa.pub'
	testconn = check_ssh()
	result = testconn.check_it(elf_staging, elf_user, key_file)
	port = 22	
	proxy_uri = "http://172.17.8.1:3128"
	url = urlparse.urlparse(proxy_uri)
	http_con = httplib.HTTPConnection(url.hostname, url.port)
	headers = {}	
	http_con.set_tunnel(elf_staging, port, headers)
	http_con.connect()
	sock = http_con.sock
	test = check_ssh(sock)
	test.check_it(elf_staging, elf_user, key_file)
	if result == True:
		print "success bitches!!!"
	else:
		print "failure bitches!!!"	