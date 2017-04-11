from Util import *
from Item import *

import re


WIKI_PATH = "./LW_Wiki.html"
RE_ITEM = r'^\s*[0-9]+\sSlot.*Leather\sPack$'

def main():
	# Read LW HTML
	wikiText = readFile(WIKI_PATH)
	wikiText = wikiText.replace("\n"," ")

	# Parse item data
	items = []
	for row in tagText("tr", wikiText):
		try:
			item = Item(row)
			items.append(item)
		except Exception, e:
			#print "Item Creation Error:", e
			pass

	# Filter unwanted items
	items = filter(lambda item: re.search(RE_ITEM, item.getTitle()), items)
	for item in items:
		c = item.getAttribute("Ingredients")
		#print item
		print c


if __name__ == '__main__':
	main()