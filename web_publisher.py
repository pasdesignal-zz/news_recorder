#!/usr/bin/python
#requires paramiko:
#sudo pip install paramiko

import paramiko
import urlparse
import httplib
import os

#To Do:
# check connectivity to ELF

class check_ssh(): #object to use for duration of bulletin creation

	def __init__(self, dest, port, user, key_file):
		self.dest = dest
		self.port = port
		self.user =user
		self.key_file = key_file
		proxy_uri = "http://172.17.8.1:3128"
		url = urlparse.urlparse(proxy_uri)
		http_con = httplib.HTTPConnection(url.hostname, url.port)
		headers = {}	
		http_con.set_tunnel(self.dest, self.port, headers)
		http_con.connect()
		self.sock = http_con.sock

	def check_it(self, initial_wait=0, interval=0, retries=1):
		ssh = paramiko.SSHClient()
		ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
		print "testing SSH connectivity to {} as user {}".format(self.dest, self.user)
		ssh.connect(self.dest, username=self.user, key_filename=self.key_file, sock=self.sock)
		return True

if __name__ == '__main__':
	elf_staging = '150.242.42.149'
	elf_port = 22
	elf_user = 'deploy'
	key_file = '/home/deploy/.ssh/id_rsa.pub'
	test = check_ssh(elf_staging, elf_port, elf_user, key_file)
	result = test.check_it()
	if result == True:
		print "success bitches!!!"
	else:
		print "failure bitches!!!"	