# Author: Mikhail Andrenkov
# Source: https://github.com/Mandrenkov/GW2_LW_Oracle

# Imports
 
from Util import *
from Item import *

class Table:
	WIDTH = 90

	def __init__(self, items):
		self.items = reversed(sorted(items))
		self.console = Console("White")

	def display(self):
		c = self.console
		self.__displayHeader(c)
		for item in self.items:
			self.__displayItem(c, item)
			self.__displayItemIngreds(c, item)
		c.writeln("-"*Table.WIDTH)
			
	def __displayHeader(self, c):
		c.writeln("-"*Table.WIDTH)
		c.writeln("|          Name             Profit      Sell       Buy           Optimal Ingredients     |")
		c.writeln("-"*Table.WIDTH)

	def __displayItem(self, c, item):
		row = c.insert("|")

		# Name
		name = getShortName(item.getName(), 22)
		row += c.insert(" %-23s " % name)

		# Profit
		profit = item.getProfit()
		row += c.insert(" %-9s " % profit, "green" if profit.isPositive() else "red")

		# Selling price
		sell = item.getSellingPrice()
		row += c.insert(" %-9s " % sell, "cyan")

		# Buying price
		buy = item.getBuyingPrice()[0]
		row += c.insert(" %-9s " % buy, "red")

		# Optimal ingredients
		quantity, ingred = item.getBuyingPrice()[1][0]
		row += c.insert(" %2d x %-23s " % (quantity, getShortName(ingred, 23)))

		row += c.insert("|")
		print row

	def __displayItemIngreds(self, c, item):
		for quantity, ingred in item.getBuyingPrice()[1][1:]:
			row = c.insert("|")
			row += " "*58
			row += c.insert(" %2d x %-23s " % (quantity, ingred))
			row += c.insert("|")
			print row