'''
Copyright 2012 Will Snook (http://willsnook.com)
MIT License

Utility code for generating antenna geometry files in nec2 card stack format
'''


# =======================================================================================================
# Placeholder strings for cards that I'm not yet generating with code
# =======================================================================================================

comments = '''
CM // NEC2 Input File
CE // End Comments
'''

config = '''
GE     0     0  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
NH     0     0     0      0  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
EX     0     5     1      0  1.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
NE     0    10     1     10 -1.35000E+00  0.00000E+00 -1.35000E+00  3.00000E-01  0.00000E+00  3.00000E-01
RP     0    19    37      0  0.00000E+00  0.00000E+00  1.00000E+01  1.00000E+01  0.00000E+00  0.00000E+00
FR     0    29     0      0  1.41000E+02  2.50000E-01  1.48000E+02  0.00000E+00  0.00000E+00  0.00000E+00
EN     0     0     0      0  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
'''

wires = '''
GW     1    15 -4.82600E-01  1.77800E-01  1.00000E-01  0.00000E+00  1.77800E-01  1.00000E-01  1.58500E-03
GW     3    15  0.00000E+00  1.77800E-01  1.00000E-01  4.88950E-01  1.77800E-01  1.00000E-01  1.58500E-03
GW     4    15  0.00000E+00  1.77800E-01  8.73000E-02 -4.82600E-01  1.77800E-01  8.73000E-02  1.58500E-03
GW     5     1  0.00000E+00  1.77800E-01  1.00000E-01  0.00000E+00  1.77800E-01  8.73000E-02  1.58500E-03
GA     6    15  6.35000E-03  9.00000E+01  2.70000E+02  1.58500E-03  1.31308E-01  0.00000E+00  0.00000E+00
GM     0     0  0.00000E+00  0.00000E+00  0.00000E+00 -4.82600E-01  1.77800E-01  9.36500E-02  6.00000E+00
'''


# =======================================================================================================
# Field formatting functions (i.e. "columns" in punchcard-speak)
# =======================================================================================================

def sci(f):
	''' Return a scientific notaion float in a 13 character wide field (xyz coordiates, radius)
	'''
	return '{: > 13.5E}'.format(f)


def dec(i):
	''' Return a decimal integer in a 6 character wide field (tags, segments)
	'''
	return '{: >6d}'.format(i)


# =======================================================================================================
# Different types of cards (see http://www.nec2.org/part_3/cards/ for card format documentation)
# =======================================================================================================

def gw(tag, segments, x1, y1, z1, x2, y2, z2, radius):
	''' Return the line for a GW card. Tag & segments have no units. Coordinates and radius are in meters.
	'''
	gw = "GW" + dec(tag) + dec(segments)
	gw += sci(x1) + sci(y1) + sci(z1)
	gw += sci(x2) + sci(y2) + sci(z2)
	gw += sci(radius)
	return gw


# =======================================================================================================
# File I/O
# =======================================================================================================

def writeCardsToFile(filename, comments, wires, config):
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


# =======================================================================================================
# Now do something useful...
# =======================================================================================================


fileName = 'foldedDiPy.nec'

writeCardsToFile(fileName, comments, wires, config)

copyCardFileToConsole(fileName)


#print gw(1,15,-0.4826,0.1778,0.1,0,0.1778,0.1,0.001585)  
#print wires
