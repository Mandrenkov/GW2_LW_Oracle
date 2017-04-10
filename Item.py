from Util import *

import re

class Component:
	def __init__(self, name, html):
		self.html = html
		self.name = name
		self.titles = []

		for title in attText("title", html):
			if len(self.titles) == 0 or self.titles[-1] != title:
				self.titles.append(title)

		quantities = tagText("dt", html)
		for index, quant in enumerate(quantities):
			self.titles[index] = "%d %s" % (int(quant), self.titles[index]) 

	def getTitle(self):
		return self.titles[0] if len(self.titles) > 0 else "<No Title>"

	def __str__(self):
		return "Component \"%s\": %s" % (self.name, self.titles)

class Item:
	COLUMNS = ("Item", "Rarity", "Discipline(s)", "Rating", "Ingredients")

	def __init__(self, html):
		self.html = html
		self.comps = {comp: None for comp in Item.COLUMNS}

		try:
			html_comps = tagText("td", html)
			for index, name in enumerate(Item.COLUMNS):
				self.comps[name] = Component(name, html_comps[index])
		except Exception, e:
			#print "Item Creation Error: %s." % e
			raise e

	def getComponent(self, comp):
		if comp not in Item.COLUMNS:
			return "Error: \"%s\" refers to an unknown component." % comp
		else:
			return self.comps[comp]

	def getTitle(self):
		return self.comps["Item"].getTitle()

	def __str__(self):
		return "Item \"%s\"" % self.getTitle()