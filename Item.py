from Util import *

import re

#COLUMNS = ("Item", "Rarity", "Discipline(s)", "Rating", "Ingredients")

class Item:
	ELEMENTS = ("Name", "URL", "Ingredients")

	def __init__(self, html):
		self.html = html
		self.elements = {}

		parser = AttributeParser()
		HTML_columns = tagText("td", html)

		if len(HTML_columns) != 5:
			raise ValueError("HTML does not depict an Item.")

		self.elements["Name"] = parser.findElements(["span", "a"], "title", HTML_columns[0])[0]
		self.elements["URL"]  = parser.findElements(["span", "a"], "href" , HTML_columns[0])[0]

		ingredient_names = parser.findElements(["div", "dl", "dd", "a"], None, HTML_columns[-1])
		ingredient_quants = parser.findElements(["div", "dl", "dt"], None, HTML_columns[-1])
		self.elements["Ingredients"] = [(q, n) for q, n in zip(ingredient_quants, ingredient_names)]

		for element in Item.ELEMENTS:
			assert self.elements[element]


	def analyze(self):
		print "Analyzing %s..." % str(self)

		

		print "Analysis Complete"

	def getAttribute(self, att):
		if att not in self.elements:
			return "Error: \"%s\" refers to an unknown attribute." % att
		else:
			return self.elements[att]

	def getAttributes(self):
		return self.elements

	def getName(self):
		return self.elements["Name"]

	def getURL(self):
		return self.elements["URL"]

	def __str__(self):
		s = "Item \"%s\"\n" % self.elements["Name"]
		for att in sorted(self.elements):
			s += "\t%s: %s\n" % (att, self.elements[att])
		return s
