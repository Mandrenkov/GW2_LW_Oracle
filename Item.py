# Author: Mikhail Andrenkov
# Source: https://github.com/Mandrenkov/GW2_LW_Oracle

# Imports

from Price import *
from Util import *

import random
import re
import sys
import time
import urllib2


# The Item class represents an item from the perspective of the GW2 TP. 
class Item:
	# Regular expressions to find information in the HTML.
	# Item ID
	RE_ID    = re.compile(r'data-type="item" data-id="([0-9]+?)"')
	# Buying price
	RE_BUY   = re.compile(r'id="buy-price" data-price="([0-9]+?)"')
	# Selling price
	RE_SELL  = re.compile(r'id="sell-price" data-price="([0-9]+?)"')
	# Ingredient quantity
	RE_QUANT = re.compile(r'<dt>\s*([0-9]+?)</dt>')
	# Ingredient name
	RE_ING   = re.compile(r'title="(.+?)"')

	# Information about leatherworking items.
	INFO_URL = "https://wiki.guildwars2.com/wiki/"
	# Database of TP market prices.
	MARKET_URL = "https://www.gw2tp.com/item/"

	# Path to the directory containing an Item's information HTML page.
	INFO_PATH = "./HTML/Info/"
	# Path to the directory containing an Item's market price HTML page.
	MARKET_PATH = "./HTML/Market/"
	# Path to the directory containing the Item listing HTML page.
	STATIC_PATH = "./HTML/Static/"
	
	# Constructs a new Item object with the given name.
	# If update is set to True, it will also fetch its ID,
	# prices, and ingredients.
	def __init__(self, name, update = True):
		self.name = name
		self.ID = -1
		# TP buying Price
		self.buy = None
		# Tuple consisting of the minimal Price required to acquire
		# this Item, as well as the ingredients associated with this
		# method of purchase.
		self.buy_cache = None
		# TP selling Price
		self.sell = None
		# Optimal crafting ingredients
		self.ingreds = []

		if update:
			self.__initID()
			self.__initPrices()
			self.__initIngreds()

	# Fetches and sets the ID of this Item.
	def __initID(self):
		html = self.__getHTML(self.getInfoPath(), self.getInfoURL())
		result = re.search(Item.RE_ID, html)
		if result:
			self.ID = int(result.group(1))
		else:
			print "Error: Unable to find ID of Item \"%s\"." % self.name
			# Each Item should have an ID.
			raise Exception("All items should have an ID")

	# Fetches and sets the market prices of this Item.
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

	# Fetches and sets the crafting ingredients for this Item.
	def __initIngreds(self):
		self.ingreds = []

		# An Item's ingredients is found between these two lines of HTML.
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

	# Returns the base file name of this Item.
	def getFileName(self):
		return self.name.replace(" ", "_")

	# Returns the path to this Item's information HTML.
	def getInfoPath(self):
		return Item.INFO_PATH + self.getFileName() + ".html"

	# Returns the URL that hosts this Item's information HTML.
	def getInfoURL(self):
		return Item.INFO_URL + self.getFileName()

	# Returns the path to this Item's market price HTML.
	def getMarketPath(self):
		return Item.MARKET_PATH + self.getFileName() + ".html"

	# Returns the URL that host this Item's market price HTML.
	def getMarketURL(self):
		return "%s%d-%s" % (Item.MARKET_URL, self.ID, self.name.lower().replace(" ", "-"))

	# Calculates and returns the minimum Price necessary to acquire
	# this item, including buying it directly from the TP or crafting it.
	def getBuyingPrice(self):
		# Returns minimal price required to purchase this Item, in addition
		# to the corresponding ingredients for this method of purchase.  
		def calculatePrice():
			# Price has already been calculated.
			if self.buy_cache:
				return self.buy_cache

			# This Item cannot be crafted.
			if len(self.ingreds) == 0:
				return (self.buy, [(1, self.name)])

			buy_price = Price(0)
			buy_list = []

			# Determine minimal Price for crafting this Item
			for quantity, name in self.ingreds:
				item = Item(name)
				sub_price, sub_ingreds = item.getBuyingPrice()
				buy_price += sub_price.getFactor(quantity)

				for sub_q, sub_n in sub_ingreds:
					buy_list.append((sub_q * quantity, sub_n))

			# Buying this Item directly from the TP is cheaper.
			if buy_price > self.buy:
				return (self.buy, [(1, self.name)])
			# Crafting this Item from its ingredients is cheaper.
			else:
				return (buy_price, buy_list)

		self.buy_cache = calculatePrice()
		#print "Buying Price of \"%s\" is: %s %s" % (self.name, self.buy_cache[0], self.buy_cache[1])
		return self.buy_cache

	# Returns the TP selling Price of this Item.
	def getSellingPrice(self):
		return self.sell

	# Returns the total TP tax incurred when selling this Item.
	def getTotalTax(self):
		return self.getListingTax() + self.getExchangeTax()

	# Returns the TP listing tax incurred when listing this Item for sale.
	def getListingTax(self):
		return self.getSellingPrice().getFactor(0.05)

	# Returns the TP exchange tax incurred when a buy purchases this Item.
	def getExchangeTax(self):
		return self.getSellingPrice().getFactor(0.10)

	# Returns the expected profit associated with this Item.
	def getProfit(self):
		return self.getSellingPrice() - self.getBuyingPrice()[0] - self.getTotalTax()

	# Returns the name of this Item
	def getName(self):
		return self.name

	# Downloads the HTML page located at the given URL and places
	# it in the directory denoted by path.  If this item has already
	# been downloaded, the existing results page is used.
	def __getHTML(self, path, url):
		if not os.path.isfile(path):
			sys.stdout.write("Fetching '%s'..." % url)
			request = urllib2.Request(url)
			request.add_header("User-agent", "Custom/4.7.0")
			content = urllib2.urlopen(request).read()
			print "done"

			# This is *not* a DoS attack
			delta = 0.5 + random.random()/2
			time.sleep(delta)

			with open(path, "w") as fout:
				fout.write(content)

		return readFile(path).replace("\n", " ")

	# Returns False if this Item generates less profit than the given Item.
	# Otherwise, True is returned.
	def __lt__(self, other):
		return self.getProfit() < other.getProfit()

	# Returns a string representation of this Item.
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
