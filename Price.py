# Author: Mikhail Andrenkov
# Source: https://github.com/Mandrenkov/GW2_LW_Oracle

# Imports

from Util import *


# The Price class denotes the value of a particular Item.
class Price:
	# Constructs a Price object.
	def __init__(self, price):
		self.price = price

	# Returns the reduced amount of copper in this Price .
	def getCopper(self):
		return self.price % 100

	# Returns the reduced amount of silver in this Price.
	def getSilver(self):
		return (self.price/100) % 100

	# Returns the amount of gold in this Price.
	def getGold(self):
		return self.price/10000

	# Returns a new Price with the value of this Price scaled by the given factor.
	def getFactor(self, factor):
		return Price(int(self.price*factor))

	# Returns True if this Price denotes a positive quantity.
	def isPositive(self):
		return self.price >= 0

	# Adds Prices together by combining their values
	def __add__(self, other):
		return Price(self.price + other.price)

	# Compares two Prices by their values
	def __cmp__(self, other):
		if self.price < other.price:
			return -1
		elif self.price == other.price:
			return 0
		else:
			return 1

	# Subtracts the value of the second Price from the value of this Price
	def __sub__(self, other):
		return Price(self.price - other.price)

	# Return a string representation of this Price
	def __str__(self):
		s = "" if self.price >= 0 else "-"

		# Ignore price negation
		price = self.price
		self.price = abs(self.price)
		s += "%02d.%02d.%02d" % (self.getGold(), self.getSilver(), self.getCopper())
		self.price = price

		return s 