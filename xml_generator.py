#!/usr/bin/python
import xml.etree.cElementTree as ET
import subprocess
from subprocess import Popen, call, PIPE
import os
import datetime
#To Do:
#Make this class handle an invalid xml file elegantly
#Element data has to be strings?

#Open XML document using ET parser.
#ET.parse takes one argument and returns a parsed 
#representation of the XML document.
#!!!!!Make this tolerate an invalid XML somehow!!!!!!!!!!######## 
class xml_machine(): 
	#Class attributes go here
	def __init__(self):
		self.programme_code = ""
		self.title = ""
		self.body = ""
		self.participants = ""
		self.duration = ""
		self.broadcast_at = ""
		self.downloadable = ""
		self.mp3_url = ""
		self.mp3_size = ""
		self.ogg_url = ""
		self.ogg_size = ""

	def parse_template(self, input_xml):
		self.input_xml = input_xml
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} opening XML: {}".format(timestamp, self.input_xml)               #debug
		self.tree = ET.parse(self.input_xml)
		#print "tree:", self.tree                           #debug
		self.root = self.tree.getroot()
		#print "root:", self.root                           #debug
		self.rootlength = len(self.root)
		print "XML file %s Root element %s has %s child elements:" % (self.input_xml, self.root.tag, self.rootlength)
		#for child in self.root:
		#	print child, child.text
		self.programme_code = self.root.find("programme_code").text
		self.title = self.root.find("title").text
		self.body = self.root.find("body").text
		self.participants = self.root.find("participants").text
		self.duration = self.root.find("duration").text
		self.broadcast_at = self.root.find("broadcast_at").text
		self.downloadable = self.root.find("downloadable").text
		self.mp3_url = self.root.find("mp3_url").text
		self.mp3_size = self.root.find("mp3_size").text
		self.ogg_url = self.root.find("ogg_url").text 
		self.ogg_size = self.root.find("ogg_size").text

#creates xml 'element tree' object which can be then written to file (no need to parse template)   
	def xml_tree(self):
		self.root = ET.Element("audio_item")
		self.tree = ET.ElementTree(self.root)
		
#writes xml object to file
	def xml_write(self, output_xml):
		self.output_xml = output_xml
		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
		print "{} writing XML to file: {}".format(timestamp, self.output_xml)  
		for element in self.root.iter():
			if element.tag == 'programme_code':
				element.text = self.programme_code
			if element.tag == 'title':
				element.text = self.title
			if element.tag == 'body':
				element.text = self.body
			if element.tag == 'participants':
				element.text = self.participants
			if element.tag == 'duration':
				element.text = self.duration
			if element.tag == 'broadcast_at':
				element.text = self.broadcast_at
			if element.tag == 'downloadable':
				element.text = self.downloadable
			if element.tag == 'mp3_url':
				element.text = self.mp3_url
			if element.tag == 'mp3_size':
				element.text = self.mp3_size
			if element.tag == 'ogg_url':
				element.text = self.ogg_url
			if element.tag == 'ogg_size':
				element.text = self.ogg_size
			self.tree.write(output_xml)

if __name__ == '__main__':
	template_xml = (os.getcwd()+'/diginews_template.xml')
	test = xml_machine()
	test.parse_template(template_xml)
	test.programme_code = " test1"
	test.title = "test2"
	test.body = "test3"
	test.participants = "test4"
	test.duration = "test5"
	test.broadcast_at = "test6"
	test.downloadable = "test7"
	test.mp3_url = "test8"
	test.mp3_size = "test9"
	test.ogg_url = "test10"
	test.ogg_size = "test11"
	test.xml_write((os.getcwd()+'/elf-test.xml'))
	#test writing xml from scratch
	#test2 = xml_machine()
	#test2.xml_tree()
	#test.ogg_url = 'testesonetwo'
	#test.ogg_size = '100'
	#test2.xml_write(os.getcwd()+'/elf-test.xml')

	#ET.SubElement(self.root , "programme_code").text = self.programme_code
	#ET.SubElement(self.root , "title").text = self.title
	#ET.SubElement(self.root , "body").text = self.body
	#ET.SubElement(self.root , "participants").text = self.participants
	#ET.SubElement(self.root , "broadcast_at").text = self.broadcast_at
	#ET.SubElement(self.root , "downloadable").text = self.downloadable
	#ET.SubElement(self.root , "mp3_url").text = self.mp3_url
	#ET.SubElement(self.root , "mp3_size").text = self.mp3_size
	#ET.SubElement(self.root , "ogg_url").text = self.ogg_url
	#ET.SubElement(self.root , "ogg_size").text = self.ogg_size