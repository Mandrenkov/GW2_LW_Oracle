from Util import *
from Item import *
from Table import *

import os
import re
import sys

CLEAR_CACHE = False

LW_PATH = "./HTML/Static/LW_Wiki.html"
#RE_ITEM = re.compile(r'"([0-9]+ Slot [A-Za-z]+ Leather Pack)"')
RE_ITEM = re.compile(r'"([0-9A-Za-z\s]+? Pack)"')


def main():
	console = Console()

	# Discover LW items
	lw_text = readFile(LW_PATH)
	item_names = sorted(set(text for text in RE_ITEM.findall(lw_text)))
	items = []

	for name in item_names:
		try:
			item = Item(name)
			if CLEAR_CACHE:
				os.system("rm %s" % item.getMarketPath())
			item = Item(name)
			items.append(item)
		except Exception, e:
			print e
			pass

	table = Table(items)
	table.display()

if __name__ == '__main__':
	main()