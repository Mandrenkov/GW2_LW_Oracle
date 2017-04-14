from ctypes import windll, c_int, byref

import os
import re

def getShortName(name, length, fill = False):
	if len(name) > length:
		name = name[:length - 3] + "..."
	if fill:
		name += " "*(length - len(name))
	return name

def readFile(path):
	contents = None
	with open(path, "r") as f_in:
		contents = f_in.read()
	return contents.replace("\n", "    ")

class Console:
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

	def __init__(self, clr = "white"):
		self.__enableANSI()
		self.clr = clr.lower()

	def insert(self, message, colour = None):
		code = self.clr if not colour else colour.lower()
		return ("\033[1;%dm" % Console.COLOUR_MAP[code]) + str(message) + "\033[0m"

	def writeln(self, message, colour = None):
		print self.insert(message, colour)

	def __enableANSI(self):
		stdout_handle = windll.kernel32.GetStdHandle(c_int(-11))
		mode = c_int(0)
		windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
		mode = c_int(mode.value | 4)
		windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)