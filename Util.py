from HTMLParser import HTMLParser

import os
import re


ATT_TEMPLATE = r'%s="(.*?)"'
TAG_TEMPLATE = r'<%s>?(.*?)</%s>'

URL_BASE = "https://wiki.guildwars2.com/wiki/"


class ProductError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class AttributeParser(HTMLParser):
	RE_IGNORE = r'img|br'

	def findElements(self, tags, name, html):
		self.stack = []
		self.target = ".".join(tags)
		self.name = name
		self.is_data = name is None

		self.elements = []
		self.feed(html)
		return self.elements

	def handle_starttag(self, tag, attrs):
		self.stack.append(tag)
		#print self.stack, attrs

		if not self.is_data and ".".join(self.stack) == self.target:
			for pair in filter(lambda pair: pair[0] == self.name, attrs):
				self.elements.append(pair[1])

		if re.search(AttributeParser.RE_IGNORE, tag):
			self.stack.pop()

	def handle_endtag(self, tag):
		self.stack.pop()
		#print self.stack

	def handle_data(self, data):
		if self.is_data and ".".join(self.stack) == self.target:
			self.elements.append(data)


def attText(attribute, html):
	regex = ATT_TEMPLATE % attribute
	return [text for text in re.findall(regex, html)]

def getShortName(name, length):
	if len(name) > length:
		name = name[:length - 3] + "..."
	return name

def readFile(path):
	contents = None
	with open(path, "r") as f_in:
		contents = f_in.read()
	return contents

def tagText(tag, html):
	regex = TAG_TEMPLATE % (tag, tag)
	return [text for text in re.findall(regex, html)]


'''
class MyHTMLParser(HTMLParser):
	def init(self):
		self.stack = []

	def handle_starttag(self, tag, attrs):
		self.stack.append(tag)

		print "Start tag:", tag, self.stack
		for attr in attrs:
			print "     attr:", attr

		if re.search(AttributeParser.RE_IGNORE, tag):
			self.stack.pop()

	def handle_endtag(self, tag):
		print "End tag  :", tag, self.stack
		self.stack.pop()

	def handle_data(self, data):
		print "Data     :", data
'''