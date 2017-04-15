# Author: Mikhail Andrenkov
# Source: https://github.com/Mandrenkov/GW2_LW_Oracle


# Imports

from Util import *
from Item import *
from Table import *

import argparse
import os
import re
import sys


# Global Variables

args = None

LW_PATH = "./HTML/Static/LW_Wiki.html"
RE_ITEM = re.compile(r'"([0-9]+ Slot [A-Za-z]+ Leather Pack)"')
RE_ITEM = re.compile(r'"([0-9A-Za-z\s]+? Pack)"')


# Global Functions

# Parses the command-line arguments and updates the global Argument object
def parseArguments():
	global args
	
	# Set description
	parser = argparse.ArgumentParser(description = "This program displays a summary of GW2 leatherworking TP prices.")
	
	# Add options	
	parser.add_argument("-c", "--clear_cache", help = "Clears the TP cache", action = "store_true")

	# Retrieve arguments
	args = parser.parse_args()


# Returns a list of names that match the RE_ITEM regex 
def retrieveItems():
	lw_text = readFile(LW_PATH)
	return sorted(set(text for text in RE_ITEM.findall(lw_text)))


# Main program entry point 
def main():
	parseArguments()

	item_names = retrieveItems()
	items = []

	for name in item_names:
		try:
			# Clear cache if specified
			if args.clear_cache:
				item = Item(name, False)
				os.system("rm %s" % item.getMarketPath())

			items.append(Item(name))
		# Unable to parse Item
		except Exception, e:
			print e

	# Display the TP summary
	table = Table(items)
	table.display()


# Initiate program
if __name__ == '__main__':
	main()