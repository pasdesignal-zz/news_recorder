#!/usr/bin/python
import xml.etree.cElementTree as ET
import subprocess
from subprocess import Popen, call, PIPE
import os

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
		print "Opening XML:", self.input_xml               #debug
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
		
##writes xml object to file
	def xml_write(self, output_xml):
		print "Writing XML to file:", output_xml
		ET.SubElement(self.root , "programme_code").text = self.programme_code
		ET.SubElement(self.root , "title").text = self.title
		ET.SubElement(self.root , "body").text = self.body
		ET.SubElement(self.root , "participants").text = self.participants
		ET.SubElement(self.root , "broadcast_at").text = self.broadcast_at
		ET.SubElement(self.root , "downloadable").text = self.downloadable
		ET.SubElement(self.root , "mp3_url").text = self.mp3_url
		ET.SubElement(self.root , "mp3_size").text = self.mp3_size
		ET.SubElement(self.root , "ogg_url").text = self.ogg_url
		ET.SubElement(self.root , "ogg_size").text = self.ogg_size
		self.tree.write(output_xml)

if __name__ == '__main__':
	template_xml = (os.getcwd()+'/diginews_template.xml')
	test = xml_machine()
	test.parse_template(template_xml)
	test.ogg_url = 'testesonetwo'
	test.ogg_size = '100'
	test.xml_write((os.getcwd()+'/elf-test.xml'))
	#test writing xml from scratch
	#test2 = xml_machine()
	#test2.xml_tree()
	#test.ogg_url = 'testesonetwo'
	#test.ogg_size = '100'
	#test2.xml_write(os.getcwd()+'/elf-test.xml')