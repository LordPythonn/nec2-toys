'''
Copyright 2012 Will Snook (http://willsnook.com)
MIT License

Use utility functions to generate a NEC2 card stack file for the driven element of a 2 element 2m
Cheap Yagi design. My goal is to produce a model that matches the 150 Ohm free space impedance
at 145MHz which Kent Britain mentioned in his "Cheap Antennas for the AMSAT LEO's" article. Assuming
I get to that point, I intend to finish out the antenna and see how the SWR looks across the 2m band.
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
EX     0     5     1      0  1.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
NE     0    10     1     10 -1.35000E+00  0.00000E+00 -1.35000E+00  3.00000E-01  0.00000E+00  3.00000E-01
RP     0    19    37      0  0.00000E+00  0.00000E+00  1.00000E+01  1.00000E+01  0.00000E+00  0.00000E+00
FR     0    29     0      0  1.41000E+02  2.50000E-01  1.48000E+02  0.00000E+00  0.00000E+00  0.00000E+00
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


# =======================================================================================================
# Make the wire cards to model the driven element of a Cheap Yagi 2 element, 2m beam.
# =======================================================================================================

'''
Wires and Arcs of the driven element that I'm trying to model...
- The '+' characters mark boundaries between GW or GA cards in the model
- A, B, C, E, F, and G are 1/8" diameter wires (one GW card for each)
- D is an arc of 1/8" diameter wire (GA card + a couple GM cards to position it)
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

woodSquareSide      = inch(0.75)
arcRadiusD          = inch(0.5)
feedpointSeparation = inch(0.5)
overallLength       = inch(38.5)
deY                 = 0.0
deTopZ              = 0.0
lengthOfBendF       = inch(2.0)

a1 = Point((overallLength-woodSquareSide)/2.0, deY, deTopZ)
a2 = Point(beamWidth/2.0, deY, deTopZ)
b1 = a2
b2 = Point(-b1.x, b1.y, b1.z)
c1 = b2
c2 = Point(0.0-(((overallLength-woodSquareSide)/2.0)-arcRadiusD), deY, deTopZ)
d  = Point(c2.x, deY, deTopZ-arcRadiusD)
e1 = Point(c2.x, deY, deTopZ-(2.0*arcRadiusD)
e2 = Point(c1.x-lengthOfBendF, deY, e1.z)
f1 = e2
f2 = Point(c1.x, deY, deTopZ-feedpointSeparation)
g1 = f2
g2 = Point(b1.x, deY, g1.z)
h1 = f2
h2 = c1





wireRadius = inch(1.0/16.0) # Radius = 1/16", diameter = 1/8"
segs = 15                  # This is what xnec2c came up with
feedpointSegs = 1          # My reading of the EZNEC's feed point docs suggests this is correct

# Need to re-derive all this stuff with formulas based on the original Cheap Yagi 2m-2element design
# All these constants are copied from the output of an attempt to do this in xnec2c's GUI
wires  = gw(1,segs         ,m(-0.4826),m(0.1778),m(0.1)   ,m(0)      ,m(0.1778),m(0.1)   ,wireRadius)
wires += gw(3,segs         ,m(0)      ,m(0.1778),m(0.1)   ,m(0.48895),m(0.1778),m(0.1)   ,wireRadius)
wires += gw(4,segs         ,m(0)      ,m(0.1778),m(0.0873),m(-0.4826),m(0.1778),m(0.0873),wireRadius)
wires += gw(5,feedpointSegs,m(0)      ,m(0.1778),m(0.1)   ,m(0)      ,m(0.1778),m(0.0873),wireRadius)
wires += ga(6,segs,inch(0.25),deg(90),deg(270),wireRadius)
wires += gm(deg(0),deg(0),deg(0),m(-0.4826),m(0.1778),m(0.09365),6)


# =======================================================================================================
# Write the file
# =======================================================================================================

fileName = 'freeSpace2mDE.nec'
writeCardsToFile(fileName, comments, wires, footer)
copyCardFileToConsole(fileName)


