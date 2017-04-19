# Author: Mikhail Andrenkov
# Source: https://github.com/Mandrenkov/GW2_LW_Oracle

# Imports

from ctypes import windll, c_int, byref

import os
import platform
import re


# Global classes

# The Console class enables coloured text to be displayed to standard output.
class Console:
	# Mapping of colour names to their respective ANSI codes
	COLOUR_MAP = {
		"black" : 30,
		"red"   : 31,
		"green" : 32,
		"yellow": 33,
		"blue"  : 34,
		"purple": 35,
		"cyan"  : 36,
		"white" : 37
	}

	# Construct a Console object with the specified default colour
	def __init__(self, clr = "white"):
		self.__enableANSI()
		self.clr = clr.lower()

	# Returns the given message with a padding to specify the provided colour
	def insert(self, message, colour = None):
		code = self.clr if not colour else colour.lower()
		return ("\033[1;%dm" % Console.COLOUR_MAP[code]) + str(message) + "\033[0m"

	# Displays the given message to standard output under the given colour
	def writeln(self, message, colour = None):
		print self.insert(message, colour)

	# Enables ANSI terminal colours on Windows
	def __enableANSI(self):
		if platform.system() == "Windows":
			stdout_handle = windll.kernel32.GetStdHandle(c_int(-11))
			mode = c_int(0)
			windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
			mode = c_int(mode.value | 4)
			windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)


# Global functions

# Returns a representation of the given name with the specified maximum length.
# Enabling fill will right-pad the returned string with spaces if necessary
def getShortName(name, length, fill = False):
	if len(name) > length:
		name = name[:length - 3] + "..."
	if fill:
		name += " "*(length - len(name))
	return name

# Returns the contents of the file from the specified path.
# To aid with regex operations, newlines are replaced with spaces.
def readFile(path):
	contents = None
	with open(path, "r") as f_in:
		contents = f_in.read()
	return contents.replace("\n", "    ")