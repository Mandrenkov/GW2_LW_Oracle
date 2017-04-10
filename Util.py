import re

ATT_TEMPLATE = r'%s="(.*?)"'
TAG_TEMPLATE = r'<%s>?(.*?)</%s>'


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