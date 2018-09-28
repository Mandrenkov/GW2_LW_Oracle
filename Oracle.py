# Author: Mikhail Andrenkov
# Source: https://github.com/Mandrenkov/GW2_LW_Oracle


# Imports

from Util import *
from Item import *
from Table import *

import argparse
import os
import re
import shutil
import sys
import urllib2

# Global Variables
PROFESSION_FILE = Item.STATIC_PATH + "Profession.html"
PROFESSION_SITE = "https://wiki.guildwars2.com/wiki/Leatherworker"
RE_ITEM = re.compile(r'"([0-9]+ Slot [A-Za-z]+ Leather Pack)"')


# Global Functions

# Parses the command-line arguments and updates the global Argument object
def parseArguments():
	# Set description
	parser = argparse.ArgumentParser(description = "This program displays a summary of GW2 leatherworking TP prices.")
	# Add options
	parser.add_argument("-c", "--clear_cache", help = "Clears the TP cache", action = "store_true")
	# Retrieve arguments
	return parser.parse_args()


# Returns a list of names that match the RE_ITEM regex 
def retrieveItems():
	lw_text = readFile(PROFESSION_FILE)
	return sorted(set(text for text in RE_ITEM.findall(lw_text)))



def setup(args):
	# Clear the cache if necessary.
	if args.clear_cache and os.path.exists(Item.MARKET_PATH):
		sys.stdout.write("Clearing the Trading Post cache...")
		shutil.rmtree(Item.MARKET_PATH)
		print "done"

	# Create the "Market" and "Info" directories.
	for path in (Item.MARKET_PATH, Item.INFO_PATH, Item.STATIC_PATH):
		if not os.path.exists(path):
			os.makedirs(path)

	# Fetch the profession information page.
	if not os.path.exists(PROFESSION_FILE):
		sys.stdout.write("Fetching '%s'..." % PROFESSION_SITE)
		request = urllib2.urlopen(PROFESSION_SITE)
		content = request.read()
		print "done"
		with open(PROFESSION_FILE, "w") as fout:
			fout.write(content)


# Main program entry point 
def main():
	args = parseArguments()
	setup(args)

	item_names = retrieveItems()
	items = []

	for name in item_names:
		try:
			items.append(Item(name))
		except Exception, e:
			# Failed to parse the current Item.
			print e

	# Display the TP summary
	table = Table(items)
	table.display()


# Initiate program
if __name__ == '__main__':
	main()