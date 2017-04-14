from Price import *
from Util import *

import random
import re
import time


class Item:
	RE_ID    = re.compile(r'data-type="item" data-id="([0-9]+?)"')
	RE_BUY   = re.compile(r'id="buy-price" data-price="([0-9]+?)"')
	RE_SELL  = re.compile(r'id="sell-price" data-price="([0-9]+?)"')
	RE_QUANT = re.compile(r'<dt>\s*([0-9]+?)</dt>')
	RE_ING   = re.compile(r'title="(.+?)"')

	INFO_URL = "https://wiki.guildwars2.com/wiki/"
	MARKET_URL = "https://www.gw2tp.com/item/"

	INFO_PATH = "./HTML/Info/"
	MARKET_PATH = "./HTML/Market/"
	
	def __init__(self, name):
		self.name = name
		self.ID = -1
		self.buy = None
		self.buy_cache = None
		self.sell = None
		self.ingreds = []

		self.__initID()
		self.__initPrices()
		self.__initIngreds()

	def __initID(self):
		html = self.__getHTML(self.getInfoPath(), self.getInfoURL())
		result = re.search(Item.RE_ID, html)
		if result:
			self.ID = int(result.group(1))
		else:
			print "Error: Unable to find ID of Item \"%s\"." % self.name
			raise Exception()

	def __initPrices(self):
		html = self.__getHTML(self.getMarketPath(), self.getMarketURL())
		result_buy = re.search(Item.RE_BUY, html)
		result_sell = re.search(Item.RE_SELL, html)

		if result_buy:
			self.buy = Price(int(result_buy.group(1)))
		else:
			print "Warning: Unable to find buying price of Item \"%s\"." % self.name

		if result_sell:
			self.sell = Price(int(result_sell.group(1)))
		else:
			print "Warning: Unable to find selling price of Item \"%s\"." % self.name

	def __initIngreds(self):
		self.ingreds = []

		START_LINE = '<div class="ingredients" style="padding-left:1em">'
		END_LINE   = '</div><div class="plainlinks"'

		try:
			html = self.__getHTML(self.getInfoPath(), self.getInfoURL())
			html_slice = html[html.index(START_LINE) + len(START_LINE) : html.index(END_LINE)]

			quantities = [int(q) for q in re.findall(Item.RE_QUANT, html_slice)]
			names = [name for name in re.findall(Item.RE_ING, html_slice)][::2]

			self.ingreds = zip(quantities, names)
		except:
			#print "Warning: \"%s\" is an atomic Item." % self.name
			pass

	def getFileName(self):
		return self.name.replace(" ", "_")

	def getInfoPath(self):
		return Item.INFO_PATH + self.getFileName() + ".html"

	def getInfoURL(self):
		return Item.INFO_URL + self.getFileName()

	def getMarketPath(self):
		return Item.MARKET_PATH + self.getFileName() + ".html"

	def getMarketURL(self):
		return "%s%d-%s" % (Item.MARKET_URL, self.ID, self.name.lower().replace(" ", "-"))

	def getBuyingPrice(self):
		def calculatePrice():
			if self.buy_cache:
				return self.buy_cache

			if len(self.ingreds) == 0:
				return (self.buy, [(1, self.name)])

			buy_price = Price(0)
			buy_list = []

			for quantity, name in self.ingreds:
				item = Item(name)
				sub_price, sub_ingreds = item.getBuyingPrice()
				buy_price += sub_price.scale(quantity)

				for sub_q, sub_n in sub_ingreds:
					buy_list.append((sub_q * quantity, sub_n))

			if buy_price > self.buy:
				return (self.buy, [(1, self.name)])
			else:
				return (buy_price, buy_list)

		self.buy_cache = calculatePrice()
		#print "Buying Price of \"%s\" is: %s %s" % (self.name, self.buy_cache[0], self.buy_cache[1])
		return self.buy_cache

	def getSellingPrice(self):
		return self.sell

	def getTotalTax(self):
		return self.getListingTax() + self.getExchangeTax()

	def getListingTax(self):
		return self.getSellingPrice().getTax(0.05)

	def getExchangeTax(self):
		return self.getSellingPrice().getTax(0.10)

	def getProfit(self):
		return self.getSellingPrice() - self.getBuyingPrice()[0] - self.getTotalTax()

	def getName(self):
		return self.name

	def __getHTML(self, path, url):
		if not os.path.isfile(path):
			print "Downloading \"%s\" ..." % url,
			os.system("wget -q -O %s %s" % (path, url))
			time.sleep(random.randint(1, 2)) # This is *not* a DoS attack
			print "Done."

		return readFile(path).replace("\n", " ")

	def __lt__(self, other):
		return self.getProfit() < other.getProfit()

	def __str__(self):
		return    "Item (ID = %d)\n" % self.ID \
				+ "    Name: %s\n" % self.name \
				+ "    Raw Buy: %s / Raw Sell: %s\n" % (self.buy, self.sell) \
				+ "    Raw Ingredients: %s\n" % self.ingreds \
				+ "    Optimal Ingredients: %s\n" % self.getBuyingPrice()[1] \
				+ "    Buy Price: %s\n" % self.getBuyingPrice()[0] \
				+ "    Sell Price: %s\n" % self.getSellingPrice() \
				+ "    Taxation: %s\n" % self.getTotalTax() \
				+ "    Profit: %s" % self.getProfit()