from Util import *

import re

COLUMNS = ("Item", "Rarity", "Discipline(s)", "Rating", "Ingredients")

class Attribute:
	def __init__(self, name, html):
		self.html = html
		self.name = name
		self.titles = []
		self.quants = {}

		for title in attText("title", html):
			if len(self.titles) == 0 or self.titles[-1] != title:
				self.titles.append(title)

		quantities = tagText("dt", html)
		for index, quantity in enumerate(quantities):
			title = self.titles[index]
			self.quants[title] = int(quantity)

	def getQuantity(self, title):
		return 0 if title not in self.quants else self.quants[title]

	def getTitle(self):
		return ", ".join(self.titles) if len(self.titles) > 0 else "<No Title>"

	def getTitles(self):
		return self.titles

	def __str__(self):
		s = "Attribute \"%s\": " % self.name

		f = id
		if len(self.quants) > 0:
			f = lambda title: "%d x %s" % (self.quants[title], title)

		s += ", ".join(map(f, self.titles))
		return s

class Item:
	def __init__(self, html):
		self.html = html
		self.attributes = {}

		HTML_attributes = tagText("td", html)
		for index, name in enumerate(COLUMNS):
			self.attributes[name] = Attribute(name, HTML_attributes[index])

	def getAttribute(self, comp):
		if comp not in COLUMNS:
			return "Error: \"%s\" refers to an unknown attribute." % comp
		else:
			return self.attributes[comp]

	def getAttributes(self):
		return self.attributes

	def getTitle(self):
		return self.attributes["Item"].getTitle()

	def __str__(self):
		return "Item \"%s\"" % self.getTitle()