# Author: Mikhail Andrenkov
# Source: https://github.com/Mandrenkov/GW2_LW_Oracle

# Imports
 
from Util import *
from Item import *


# The Table class displays a summary of the given list of Items. 
class Table:
	# Terminal width
	WIDTH = 90

	# Constructs a Table object with the given list of items
	def __init__(self, items):
		self.items = reversed(sorted(items))
		self.console = Console("White")

	# Displays the Item summary.
	def display(self):
		c = self.console
		self.__displayHeader(c)
		for item in self.items:
			self.__displayItem(c, item)
			self.__displayItemIngreds(c, item)
		c.writeln("-"*Table.WIDTH)
			
	# Displays the header row of the summary table.
	def __displayHeader(self, c):
		# Width of header string should be the same as WIDTH
		c.writeln("-"*Table.WIDTH)	
		c.writeln("|          Name             Profit      Sell       Buy           Optimal Ingredients     |")
		c.writeln("-"*Table.WIDTH)

	# Displays a row denoting to the given Item.
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

	# Displays the optimal ingredients to acquire the given Item. 
	def __displayItemIngreds(self, c, item):
		# The first ingredient is already displayed when __displayItem() is called.
		for quantity, ingred in item.getBuyingPrice()[1][1:]:
			row = c.insert("|")
			row += " "*58
			row += c.insert(" %2d x %-23s " % (quantity, getShortName(ingred, 23)))
			row += c.insert("|")
			print row