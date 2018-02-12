#!/usr/bin/python

import xml.etree.cElementTree as ET
import subprocess
from subprocess import Popen, call, PIPE
import os


#Improvements:
#Make this class handle an invalid xml file elegantly

#Returns an xml manipulator object
#requires string variable which should be path to template xml
class xml_machine():
	 
	 ##Class attributes go here
	 #Open XML document using ET parser.
	#ET.parse takes one argument and returns a parsed 
	#representation of the XML document.
	#!!!!!Make this tolerate an invalid XML somehow!!!!!!!!!!######## 
	def __init__(self):
		pass 			#is this a legit way to do this?????

	def parse_template(self, input_xml):
		self.input_xml = input_xml
		print "Opening XML:", self.input_xml               #debug
		self.tree = ET.parse(self.input_xml)
		print "tree:", self.tree                           #debug
		self.root = self.tree.getroot()
		print "root:", self.root                           #debug
		self.rootlength = len(self.root)
		print "XML file %s Root element %s has %s child elements:" % (self.input_xml, self.root.tag, self.rootlength)
		for child in self.root:
			print child, child.text
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


#ET.SubElement(SS , "essid").text = "%s" % (self.name)
###WRITE####t
#creates xml 'element tree' object which can be then written to file    
#This could be improved and made more modular
	def xml_tree(self):
		root = ET.Element("audio_item")
		code = ET.SubElement(root, "programme_code")
		title = ET.SubElement(root, "title")
		body = ET.SubElement(root, "body")
		participants = ET.SubElement(root, "participants")
		duration = ET.SubElement(root, "duration")
		ba = ET.SubElement(root, "broadcast_at")
		downloadable = ET.SubElement(root, "downloadable")
		mp3_url = ET.SubElement(root, "mp3_url")
		mp3_size = ET.SubElement(root, "mp3_size")
		ogg_url = ET.SubElement(root, "ogg_url")
		ogg_size = ET.SubElement(root, "ogg_size")
		ET.SubElement(root , "programme_code").text = "testesonetwo"
		self.tree = ET.ElementTree(root)

##writes xml object to file
#requires string for output file destination/name
	def xml_write(self, output_xml):
		#print "Writing XML to file:", output_xml
		self.tree.write(output_xml)

if __name__ == '__main__':
	template_xml = (os.getcwd()+'/diginews_template.xml')
	test = xml_machine()
	test.parse_template(template_xml)
	test.xml_write(os.getcwd()+'/elf-test.xml')
	#test writing xml from scratch
	#test.xml_tree()
	test.xml_tree()
	test.xml_write((os.getcwd()+'/elf-test2.xml'))



