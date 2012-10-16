'''
Copyright 2012 Will Snook (http://willsnook.com)
MIT License

Utility code for generating antenna geometry files in nec2 card stack format
'''

import math


# =======================================================================================================
# Field formatting functions (i.e. "columns" in punchcard-speak)
# =======================================================================================================

def sci(f):
	''' Return formatted string containinga scientific notaion float in a 13 char wide field (xyz coordiates, radius)
	'''
	return '{: > 13.5E}'.format(f)


def dec(i):
	''' Return formatted string containing a decimal integer in a 6 char wide field (tags, segments)
	'''
	return '{: >6d}'.format(i)


# =======================================================================================================
# Unit conversions... The nec2 engine requires its inputs to be in meters and degrees.
# =======================================================================================================

def m2m(m):
	''' Convert meters to meters. Useful for being consistent about always specifying units and for
		making sure not to accidentaly run afoul of Python's integer math (hence the * 1.0)
	'''
	return m * 1.0

def cm2m(cm):
	''' Convert cm to meters
	'''
	return cm / 100.0

def ft2m(i):
	''' Convert feet to meters
	'''
	return i * 12.0 * 2.54 / 100.0

def in2m(i):
	''' Convert inches to meters
	'''
	return i * 2.54 / 100.0

def deg2deg(degrees):
	''' Convert degrees to degrees
	'''
	return degrees * 1.0


# =======================================================================================================
# Different types of cards (see http://www.nec2.org/part_3/cards/ for card format documentation)
# Tag & segments have no units. Dimensions are in meters. Angles are in degrees.
# =======================================================================================================

def gw(tag, segments, x1, y1, z1, x2, y2, z2, radius):
	''' Return the line for a GW card, a wire.
	'''
	gw = "GW" + dec(tag) + dec(segments)
	gw += sci(x1) + sci(y1) + sci(z1)
	gw += sci(x2) + sci(y2) + sci(z2)
	gw += sci(radius) + "\n"
	return gw

def ga(tag, segments, arcRadius, startAngle, endAngle, wireRadius):
	''' Return the line for a GA card, an arc in the X-Z plane with it's center at the origin
	'''
	notUsed = 0.0
	ga = "GA" + dec(tag) + dec(segments)
	ga += sci(arcRadius) + sci(startAngle) + sci(endAngle)
	ga += sci(wireRadius)
	ga += sci(notUsed) # Note: xnec2c fills this in with it's "Segs % lambda" field, but that may be a bug
	ga += sci(notUsed) + sci(notUsed) + "\n"
	return ga

def gm(rotX, rotY, rotZ, trX, trY, trZ, firstTag):
	''' Return the line for a GM card, move (rotate and translate).
		rotX, rotY, and rotZ: angle to rotate around each axis
		trX, trY, and trZ: distance to translate along each axis
		firstTag: first tag# to apply transform to (subseqent tag#'s get it too... like it or not)
	'''
	tagIncrement = 0
	newStructures = 0
	gm = "GM" + dec(tagIncrement) + dec(newStructures)
	gm += sci(rotX) + sci(rotY) + sci(rotZ)
	gm += sci(trX) + sci(trY) + sci(trZ)
	gm += sci(firstTag*1.0) + "\n"
	return gm


# =======================================================================================================
# File I/O
# =======================================================================================================

def writeCardsToFile(fileName, comments, wires, config):
	''' Write a NEC2 formatted card stack to the output file
	'''
	nec2File = open(fileName,'w')
	nec2File.write(comments.strip() + "\n")
	nec2File.write(   wires.strip() + "\n")
	nec2File.write(  config.strip() + "\n")
	nec2File.close()


def copyCardFileToConsole(fileName):
	''' Dump the card stack back to the console for a quick sanity check
	'''
	nec2File = open(fileName,'r')
	print nec2File.read(),
	nec2File.close()


