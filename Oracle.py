from Util import *
from Item import *

import re
import traceback


WIKI_PATH = "./HTML/Static/LW_Wiki.html"
RE_ITEM = r'^\s*[0-9]+\sSlot.*Leather\sPack$'


def main():
	# Read LW HTML
	wikiText = readFile(WIKI_PATH)
	wikiText = wikiText.replace("\n"," ")

	# Parse item data
	products = []
	for row in tagText("tr", wikiText):
		try:
			product = Product(row)
			products.append(product)
		except ProductError, e:
			pass
		except Exception, e:
			print traceback.format_exc()

	# Filter unwanted items
	products = filter(lambda product: re.search(RE_ITEM, product.getName()), products)

	for product in products:
		product.analyze()

	print
	print "-"*20
	print "Best Product"
	print "------------\n"
	max(products).analyze()


if __name__ == '__main__':
	main()