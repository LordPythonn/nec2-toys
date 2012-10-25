'''
Copyright 2012 Will Snook (http://willsnook.com)
MIT License

Use utility functions to generate a NEC2 card stack file for a 2 element 2m
Cheap Yagi design.

I'm trying to optimize this one for transmitting on 146.310 MHz.
'''

from nec2utils import *


# =======================================================================================================
# Strings for the boilerplate stuff that I'm not generating in code (maybe I should do FR though...)
# =======================================================================================================

comments = '''
CM // NEC2 Input File
CE // End Comments
'''

footer = '''
GE     0     0  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
NH     0     0     0      0  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
EX     0     8     1      0  1.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
NE     0    10     1     10 -1.35000E+00  0.00000E+00 -1.35000E+00  3.00000E-01  0.00000E+00  3.00000E-01
RP     0    19    37      0  0.00000E+00  0.00000E+00  1.00000E+01  1.00000E+01  0.00000E+00  0.00000E+00
FR     0    13     0      0  1.43000E+02  5.00000E-01  1.49000E+02  0.00000E+00  0.00000E+00  0.00000E+00
EN     0     0     0      0  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
'''

# =======================================================================================================
# 3D point class
# =======================================================================================================

class Point:
	def __init__(self,x,y,z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

class Model:
	def __init__(self, wireRadius):
		self.text = ""
		self.wireRadius = wireRadius

	def addWire(self, tag, segments, point1, point2):
		self.text += gw(tag, segments, point1.x, point1.y, point1.z, point2.x, point2.y, point2.z, self.wireRadius)

	def getText(self):
		return self.text


# =======================================================================================================
# Make the wire cards to model the driven element of a Cheap Yagi 2 element, 2m beam.
# =======================================================================================================

'''
Wires and Arcs of the driven element that I'm trying to model...
- The '+' characters mark boundaries between GW or GA cards in the model
- A, B, C, E, F, and G are 1/8" diameter wires (one GW card for each)
- D is an arc of 1/8" diameter wire (GA card + a GM card to position it)
- H is a single segment wire to model the feedpoint (GW card + an EX card, linked by tag #)
- In terms of the GW card docs, a1 is the point (XW1, YW1, ZW1), a2 is (XW2, YW2, ZW2), and
  so on for b1, b2, ... (see http://www.nec2.org/part_3/cards/gw.html)
- For the arc, d marks the arc's center point. The convoluted way NEC2 forces you to specify
  arcs (arc radius on the GA card, positioning with a GM card), makes d's usage a bit messy
- Origin is at o, in the middle of wire B
- Coordinate system is what xnec2c uses... putting the back of your right hand against your
  monitor with your thumb pointed up, your index finger pointed left, and your middle
  finger pointed at you... thumb is +Z, index is +X, middle is +Y


                 A                        B    c1                   C                   c2 
-------------------------------------+----o---+-------------------------------------------+-,
a1                                 a2 b1    b2|h2                                            \
      ^                                     H |                                               \
      |+z                                     |h1                                         d   | D
  +x  |                              ---------+---___                                         /
<-----+                              g2  G  g1 f2    ---___                                  /
                                                    F    f1+------------------------------+-'
                                                            e2              E           e1
Constraints:
  B = G = Width of square wooden beam, the article used, article specifies 0.75"
  H = Side of beam - 2 wire radii and the thickness of wood outside the wires, I'm guessing 0.5"
  Overall Length of DE = 38.5" = A + B + C + (radius of D)
  (radius of D) = 0.5"
'''

refY				= 0.0
refZ                = inch(24.0)
refLength           = inch(40.5)

woodSquareSide      = inch(0.75)
arcRadiusD          = inch(0.5)
feedpointSeparation = inch(0.5)
deLength            = inch(38.1)
deY                 = inch(5.8)
deTopZ              = refZ
lengthOfBendF       = inch(2.0)

a1 = Point((deLength-woodSquareSide)/2.0, deY, deTopZ)
a2 = Point(woodSquareSide/2.0, deY, deTopZ)
b1 = a2
b2 = Point(-b1.x, b1.y, b1.z)
c1 = b2
c2 = Point(0.0-(((deLength-woodSquareSide)/2.0)-arcRadiusD), deY, deTopZ)
d  = Point(c2.x, deY, deTopZ-arcRadiusD)
e1 = Point(c2.x, deY, deTopZ-(2.0*arcRadiusD))
e2 = Point(c1.x-lengthOfBendF, deY, e1.z)
f1 = e2
f2 = Point(c1.x, deY, deTopZ-feedpointSeparation)
g1 = f2
g2 = Point(b1.x, deY, g1.z)
h1 = f2
h2 = c1


wireRadius = inch(1.0/16.0) # radius for a 1/8" wire
segs = 15                  # This is what xnec2c came up with, so I'm copying it
feedpointSegs = 1          # My reading of the EZNEC's feed point docs suggests this is correct

m = Model(wireRadius)
# Reflector
m.addWire(1, segs, Point(refLength/2.0, refY, refZ), Point(-(refLength/2.0), refY, refZ))

# Driven element
m.addWire(2, segs, a1, a2)
m.addWire(3, segs, b1, b2)
m.addWire(4, segs, c1, c2)
m.addWire(5, segs, e1, e2)
m.addWire(6, segs, f1, f2)
m.addWire(7, segs, g1, g2)
m.addWire(8, feedpointSegs, h1, h2)
wires = m.getText()

# Using the highest tag # for the arc so I don't have to deal with multiple GM card transforms
arcTag   = 9
arcStart = deg(90)
arcEnd   = deg(270)
wires += ga(arcTag, segs, arcRadiusD, arcStart, arcEnd, wireRadius)
wires += gm(deg(0),deg(0),deg(0), d.x, d.y, d.z, arcTag)


# =======================================================================================================
# Write the file
# =======================================================================================================

fileName = 'nec-2m-2el-146.310.nec'
writeCardsToFile(fileName, comments, wires, footer)
copyCardFileToConsole(fileName)


