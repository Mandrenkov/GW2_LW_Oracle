from Price import *
from Util import *

import re


__metaclass__ = type



class Item:
	RE_ID = r'data-type="item" data-id="([0-9]+?)"'
	RE_PRICE = r'id="%s-price" data-price="([0-9]+?)"'

	INFO_BASE_URL = "https://wiki.guildwars2.com/wiki/"
	MARKET_BASE_URL = "https://www.gw2tp.com/item/"
	
	def __init__(self, name):
		self.name = name

		self.ID = -1
		self.html_info = None
		self.html_market = None
		self.url_info = None
		self.url_market = None
		self.prices = None

		self.url_info = Item.INFO_BASE_URL + self.name.replace(" ", "_")


	def findID(self):
		if self.ID != -1:
			return self.ID

		result = re.search(Item.RE_ID, self.getHTMLInfo())
		if result:
			self.ID = int(result.group(1))
		else:
			print "Warning: Unable to find Item ID."
			return None

		return self.ID

	def findPrices(self):
		if self.prices:
			return self.prices

		if self.ID == -1:
			print "Warning: Unable to retrieve Item prices (Invalid ID)."
			return None

		self.prices = {"Buy": None, "Sell": None}

		for price in self.prices:
			result = re.search(Item.RE_PRICE % price.lower(), self.getHTMLMarket())
			if result:
				self.prices[price] = Price(int(result.group(1)))
			else:
				print "Warning: Unable to find Item %s price." % price

		return self.prices


	def getHTMLInfo(self):
		if self.html_info:
			return self.html_info

		path = "./HTML/%s_Info.html" % self.name.replace(" ", "_")
		url = self.url_info
		self.html_info = self.__getHTML(path, url) 
		return self.html_info

	def getHTMLMarket(self):
		if self.html_market:
			return self.html_market

		if self.ID == -1:
			print "Warning: Unable to retrieve Item price HTML (Invalid ID)."
			return None

		if not self.url_market:
			self.url_market = "%s%d-%s" % (Item.MARKET_BASE_URL, self.ID, self.name.lower().replace(" ", "-"))
		
		path = "./HTML/%s_Market.html" % self.name.replace(" ", "_")
		url = self.url_market
		self.html_market = self.__getHTML(path, url) 
		return self.html_market


	def __getHTML(self, path, url):
		if not os.path.isfile(path):
			os.system("curl -o %s %s" % (path, url))

		return readFile(path).replace("\n", " ")


class Product(Item):
	ELEMENTS = ("Name", "URL", "Ingredients")

	def __init__(self, html):
		self.html = None
		self.elements = {}

		parser = AttributeParser()
		HTML_columns = tagText("td", html)

		try:
			self.elements["Name"] = parser.findElements(["span", "a"], "title", HTML_columns[0])[0]
			self.elements["URL"]  = parser.findElements(["span", "a"], "href", HTML_columns[0])[0]

			ingredient_names = parser.findElements(["div", "dl", "dd", "a"], None, HTML_columns[-1])
			ingredient_quants = parser.findElements(["div", "dl", "dt"], None, HTML_columns[-1])
			self.elements["Ingredients"] = [(int(q), n) for q, n in zip(ingredient_quants, ingredient_names)]

			for element in Product.ELEMENTS:
				assert self.elements[element]

		except Exception, e:
			raise ProductError("HTML does not depict a Product.")

		super(Product, self).__init__(self.elements["Name"])

	def analyze(self):
		print "Analyzing \"%s\"..." % str(self.elements["Name"])

		if not self.findID():
			print "Failed to obtain Product ID."
			return None

		if not self.findPrices():
			print "Failed to obtain Product prices."
			return None

		ingredients = []
		for quantity, name in self.elements["Ingredients"]:
			ingredient = Item(name)
			if not ingredient.findID():
				print "Failed to obtain Ingredient \"%s\" ID." % name
				return None

			if not ingredient.findPrices():
				print "Failed to obtain Ingredient \"%s\" prices." % name
				return None

			ingredients.append((quantity, ingredient.prices["Buy"]))
			print "\tIngredient \"%-25s\" Buy Price = %2d x %s" % (getShortName(name, 25), quantity, ingredient.prices["Buy"])

		buy = Price(0)
		for quantity, price in ingredients:
			for q in xrange(quantity):
				buy += price
		
		sell = self.prices["Sell"]

		list_fee = sell.getTax(0.05)
		exch_fee = sell.getTax(0.10)

		profit = sell - list_fee - exch_fee - buy

		print "\n\tProduct Buy Price = %s" % buy
		print "\tProduct Sell Price = %s\n" % sell

		print "\tListing Fee = %s" % list_fee
		print "\tExchange Fee = %s\n" % exch_fee

		print "\tProfit = %s" % profit
		print "Analysis Complete\n"

	def getElement(self, att):
		if att not in self.elements:
			return "Error: \"%s\" refers to an unknown element." % att
		else:
			return self.elements[att]

	def getElements(self):
		return self.elements

	def getHTMLName(self):
		return self.html_name

	def getName(self):
		return self.elements["Name"]

	def getURL(self):
		return self.elements["URL"]

	def __str__(self):
		s = "Product (ID %d)\n" % self.ID
		for att in sorted(self.elements):
			s += "\t%12s: %s\n" % (att, self.elements[att])
		
		if self.ID != -1:
			s += "\n"
			for p in sorted(self.prices):
				s += "\t%12s: %s\n" % (p, self.prices[p])

		return s
