from Util import *
from Item import *

import re
import sys

LW_PATH = "./HTML/Static/LW_Wiki.html"
RE_ITEM = re.compile(r'"([0-9]+ Slot [A-Za-z]+ Leather Pack)"')
RE_ITEM = re.compile(r'"([0-9A-Za-z\s]+? Pack)"')


def main():
	# Discover LW items
	lw_text = readFile(LW_PATH)
	item_names = sorted(set(text for text in RE_ITEM.findall(lw_text)))
	items = []

	for name in item_names:
		try:
			items.append(Item(name))
		except:
			pass

	for item in sorted(items):
		print item
		print

if __name__ == '__main__':
	main()