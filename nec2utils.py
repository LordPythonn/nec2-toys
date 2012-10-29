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
# Unit conversions... The nec2 engine requires its inputs to be in meters and degrees. Note that these
# functions are named to denote the pre-conversion units, because I consider those more suitable for
# the calculations I will be working with.
# =======================================================================================================

def m(m):
	''' Convert meters to meters. Useful for being consistent about always specifying units and for
		making sure not to accidentaly run afoul of Python's integer math (hence the * 1.0)
	'''
	return m * 1.0

def inch(i):
	''' Convert inches to meters
	'''
	return i * 2.54 / 100.0

def deg(degrees):
	''' Make sure degrees are float
	'''
	return degrees * 1.0

# =======================================================================================================
# Output conversions from meters back to inches
# =======================================================================================================

def mToIn(meters):
	''' Convert meters back to inches for output in the comment section
	'''
	return meters * 100.0 / 2.54

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
	''' Return the line for a GA card, an arc in the X-Z plane with its center at the origin
	'''
	notUsed = 0.0
	ga = "GA" + dec(tag) + dec(segments)
	ga += sci(arcRadius) + sci(startAngle) + sci(endAngle)
	ga += sci(wireRadius)
	ga += sci(notUsed) # Note: xnec2c fills this in with its "Segs % lambda" field, but that may be a bug
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

def ge():
	''' Card to "terminate reading of geometry data cards"
	'''
	GPFLAG = 0  # Ground plane flag. 0 means no ground plane present.
	ge = "GE"
	ge += dec(GPFLAG) + "\n"
	return ge

def fr(start, stepSize, stepCount):
	''' Define the frequency range to be modeled
	'''
	IFRQ = 0           # Step type, 0 is linear (additive), 1 = multiplicative
	NFRQ = stepCount   # Number of frequency steps
	I3   = 0           # blank
	I4   = 0           # blank
	FMHZ   = start     # Starting frequency in MHz
	DELFRQ = stepSize  # Frequency stepping increment (IFRQ=0), or multiplication factor (IFRQ=1)
	fr = "FR"
	fr += dec(IFRQ) + dec(NFRQ) + dec(I3) + dec(I4)
	fr += sci(FMHZ) + sci(DELFRQ) + "\n"
	return fr

def ex(tag,segment):
	''' Define excitation parameters.
	'''
	I1 = 0        # Excitation type. 0 means an "applied-E-field" voltage source
	I2 = tag      # Tag number of the wire element to which the source will be applied
	I3 = segment  # Segment within the previously specified wire element to which the source will be applied
	I4 = 0        # 0 means use defaults for admittance matrix asymmetry and printing input impedance voltage
	F1 = 1.0      # Real part of voltage
	F2 = 0.0      # Imaginary part of voltage
	ex = "EX"
	ex += dec(I1) + dec(I2) + dec(I3) + dec(I4)
	ex += sci(F1) + sci(F2) + "\n"
	return ex


def rp():
	''' Card to initiate calculation and output of radiation pattern.
	'''
	I1  = 0      # 0 is normal mode: defaults to free-space unless a previous GN card specified a ground plane
	NTH = 37     # Number of values of theta (angle away from positive Z axis)
	NPH = 37     # Number of values of phi (angle away from X axis in the XY plane)
	I4  = 0      # Use defaults for some misc output printing options
	THETS = 0.0  # Theta start value in degrees
	PHIS  = 0.0  # Phi start value in degrees
	DTH   = 10.0 # Delta-theta in degrees
	DPH   = 10.0 # Delta-phi in degrees
	rp = "RP"
	rp += dec(I1) + dec(NTH) + dec(NPH) + dec(I4)
	rp += sci(THETS) + sci(PHIS) + sci(DTH) + sci(DPH) + "\n"
	return rp


def en():
	''' Card to mark end of input
	'''
	return "EN\n"


# =======================================================================================================
# 3D point and rotation classes
# =======================================================================================================

class Point:
	def __init__(self,x,y,z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)


class Rotation:
	def __init__(self,rx,ry,rz):
		self.rx = float(rx)
		self.ry = float(ry)
		self.rz = float(rz)


# =======================================================================================================
# Model class
# =======================================================================================================

class Model:
	def __init__(self, wireRadius):
		''' Prepare the model with the given wire radius
		'''
		self.wires      = ""
		self.transforms = ""
		self.wireRadius = wireRadius
		self.tag        = 0
		self.tagForEX   = 0

	def addWire(self, segments, point1, point2):
		''' Append a wire, increment the tag number, and return this object to facilitate a chained attachToEX() call
		'''
		self.tag += 1
		self.wires += gw(self.tag, segments, point1.x, point1.y, point1.z, point2.x, point2.y, point2.z, self.wireRadius)
		return self

	def addArc(self, segments, radius, start, end, rotate, translate):
		''' Append an arc using a combination of a GA card (radius, start angle, end angle), a GM card to rotate
			and translate the arc from the origin into it's correct location, and a second GM card to restore the
			transformation matrix for cards that come after the arc.
		'''
		# Place the arc in the XZ plane with its center on the origin
		self.tag += 1
		self.wires += ga(self.tag, segments, radius, start, end, self.wireRadius)
		# Move the arc to where it's supposed to be (note the tag #)
		self.transforms += gm(rotate.rx, rotate.ry, rotate.rz, translate.x, translate.y, translate.z, self.tag)
		# Restore the coordinate system (note the use of tag # + 1)
		self.transforms += gm(-rotate.rx, -rotate.ry, -rotate.rz, -translate.x, -translate.y, -translate.z, self.tag+1)
		return self

	def attachToEX(self):
		''' Tell the model to remember the current tag number for use with the EX voltage source card
		'''
		self.tagForEX = self.tag

	def getText(self, start, stepSize, stepCount):
		footer = ge()
		footer += ex(tag=self.tagForEX, segment=1)
		footer += fr(start, stepSize, stepCount)
		footer += rp()
		footer += en()
		return self.wires + self.transforms + footer


# =======================================================================================================
# File I/O
# =======================================================================================================

def writeCardsToFile(fileName, comments, wires, footer):
	''' Write a NEC2 formatted card stack to the output file
	'''
	nec2File = open(fileName,'w')
	nec2File.write(comments.strip() + "\n")
	nec2File.write(   wires.strip() + "\n")
	nec2File.write(  footer.strip() + "\n")
	nec2File.close()


def copyCardFileToConsole(fileName):
	''' Dump the card stack back to the console for a quick sanity check
	'''
	nec2File = open(fileName,'r')
	print nec2File.read(),
	nec2File.close()


