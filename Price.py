from Util import *

class Price:
	def __init__(self, price):
		self.price = price

	def getCopper(self):
		return self.price % 100

	def getSilver(self):
		return (self.price/100) % 100

	def getGold(self):
		return self.price/10000

	def getTax(self, tax):
		return Price(int(self.price*tax))

	def scale(self, factor):
		return Price(int(self.price*factor))

	def __add__(self, other):
		return Price(self.price + other.price)

	def __cmp__(self, other):
		if self.price < other.price:
			return -1
		elif self.price == other.price:
			return 0
		else:
			return 1

	def __sub__(self, other):
		return Price(self.price - other.price)

	def __str__(self):
		s = "" if self.price >= 0 else "-"

		price = self.price
		self.price = abs(self.price)
		s += "%02d.%02d.%02d" % (self.getGold(), self.getSilver(), self.getCopper())
		self.price = price

		return s 