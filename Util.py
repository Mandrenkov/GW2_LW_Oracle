from HTMLParser import HTMLParser

import re


ATT_TEMPLATE = r'%s="(.*?)"'
TAG_TEMPLATE = r'<%s>?(.*?)</%s>'


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

		if not self.is_data and ".".join(self.stack) == self.target:
			for pair in filter(lambda pair: pair[0] == self.name, attrs):
				self.elements.append(pair[1])

		if re.search(AttributeParser.RE_IGNORE, tag):
			self.stack.pop()

	def handle_endtag(self, tag):
		self.stack.pop()

	def handle_data(self, data):
		if self.is_data and ".".join(self.stack) == self.target:
			self.elements.append(data)


def attText(attribute, html):
	regex = ATT_TEMPLATE % attribute
	return [text for text in re.findall(regex, html)]

def readFile(path):
	contents = None
	with open(path, "r") as f_in:
		contents = f_in.read()
	return contents

def tagText(tag, html):
	regex = TAG_TEMPLATE % (tag, tag)
	return [text for text in re.findall(regex, html)]