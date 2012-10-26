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

'''
Wide FR:
FR     0    13     0      0  1.43000E+02  5.00000E-01  1.49000E+02  0.00000E+00  0.00000E+00  0.00000E+00
Narrow FR:
FR     0    11     0      0  1.45000E+02  2.00000E-01  1.47000E+02  0.00000E+00  0.00000E+00  0.00000E+00
Narrower FR:
FR     0    15     0      0  1.45410E+02  1.00000E-01  1.46710E+02  0.00000E+00  0.00000E+00  0.00000E+00
'''
footer = '''
GE     0     0  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
NH     0     0     0      0  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
EX     0     5     1      0  1.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00
NE     0    10     1     10 -1.35000E+00  0.00000E+00 -1.35000E+00  3.00000E-01  0.00000E+00  3.00000E-01
RP     0    19    37      0  0.00000E+00  0.00000E+00  1.00000E+01  1.00000E+01  0.00000E+00  0.00000E+00
FR     0    15     0      0  1.45410E+02  1.00000E-01  1.46710E+02  0.00000E+00  0.00000E+00  0.00000E+00
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
- A, B, D are 1/8" diameter wires (one GW card for each)
- C is an arc of 1/8" diameter wire, center at c, radius of rc (GA card + a GM card to position it)
- E is a single segment wire to model the feedpoint (GW card + an EX card, linked by tag #)
- In terms of the GW card docs, a1 is the point (XW1, YW1, ZW1), a2 is (XW2, YW2, ZW2), and
  so on for b1, b2, ... (see http://www.nec2.org/part_3/cards/gw.html)
- Origin is where a2 meets b1 and e2
- Coordinate system is what xnec2c uses... putting the back of your right hand against your
  monitor with your thumb pointed up, your index finger pointed left, and your middle
  finger pointed at you... thumb is +Z, index is +X, middle is +Y


a1               A                    a2  b1                      B                     b2 
-----------------------------------------+------------------------------------------------+-,
a1                                       |e2                                                 \
                                       E |                                                c rc| C
                                         |e1                                                 /
                                         +------------------------------------------------+-'
                                          d2                      D                     d1
Constraints:
  Total Length of wire in driven element = 3/4 wavelength at target frequency
  A + B + (pi * rc) + D = 3/4 wavelength of target frequency (length of DE)
  A = B + (pi * rc) + D
  E is less than the width of the wooden beam so that holes can be drilled for the wires (must be <= 0.5 inches)
'''

refY				= 0.0
refZ                = inch(24.0)
#refLength           = inch(40.0 + (3.0/8.0))
refLength           = inch(40.0 + (2.0/8.0))

targetMHz           = 146.310
velocityFactor      = 0.937   # This is what seems to work from trial and error simulations with 1/8" wires
quarterWavelength   = m((300.0 * 0.937) / targetMHz) / 4.0 
arcRadiusC          = inch(0.25)
#deY                 = inch(5.0 + (3.0/8.0))
deY                 = inch(5.0 + (2.0/8.0))
deTopZ              = refZ
bLength             = ((2.0*quarterWavelength) - (math.pi*arcRadiusC)) / 2.0

comments  = 'CM ----------------------------------------------------------------------------------\n'
comments += 'CM  NEC2 model for simulating a 2-element 2m Yagi built from copper wire on a wooden\n'
comments += 'CM  beam in the style of WA5VJB\'s Cheap Yagi designs.\n'
comments += 'CM  \n'
comments += 'CM  Driven element (DE) geometry, reflector (REF) to DE spacing, and REF length are\n'
comments += 'CM  tuned for min SWR at {:.3f} MHz\n'.format(targetMHz)
comments += 'CM  \n'
comments += 'CM  REF length                     = {: >6.3f} in\n'.format(mToIn(refLength))
comments += 'CM  REF to DE spacing              = {: >6.3f} in\n'.format(mToIn(deY))
comments += 'CM  DE length before bending the J = {: >6.3f} in\n'.format(mToIn(3.0*quarterWavelength))
comments += 'CM  Unbent end of DE to feedpoint  = {: >6.3f} in\n'.format(mToIn(quarterWavelength))
comments += 'CM  Radius of bend in J            = {: >6.3f} in\n'.format(mToIn(arcRadiusC))
comments += 'CM ----------------------------------------------------------------------------------\n'
comments += 'CE'
#preComments += 'CM 1/4 wavelength in inches = ' + (quarterWavelength * 100.0 / 2.54) + "\n"
#preComments += 'CM 3/4 wavelength in inches = ' + (quarterWavelength * 3.0 * 100.0 / 2.54) + "\n"

a1 = Point(quarterWavelength, deY, deTopZ)
a2 = Point(0.0, deY, deTopZ)
b1 = a2
b2 = Point(-bLength, b1.y, b1.z)
c  = Point(b2.x, deY, deTopZ-arcRadiusC)
d1 = Point(b2.x, deY, deTopZ-(2.0*arcRadiusC))
d2 = Point(a2.x, deY, d1.z)
e1 = d2
e2 = a2


wireRadius = inch(1.0/16.0) # radius for a 1/8" wire
segs = 25
arcSegs = 15
feedpointSegs = 1           # My reading of the EZNEC's feed point docs suggests this is how to attach coax

m = Model(wireRadius)
# Reflector
m.addWire(1, segs, Point(refLength/2.0, refY, refZ), Point(-(refLength/2.0), refY, refZ))

# Driven element
m.addWire(2, segs, a1, a2)
m.addWire(3, segs, b1, b2)
m.addWire(4, segs, d1, d2)
m.addWire(5, feedpointSegs, e1, e2)
wires = m.getText()

# Using the highest tag # for the arc so I don't have to deal with multiple GM card transforms
arcTag   = 7
arcStart = deg(90)
arcEnd   = deg(270)
wires += ga(arcTag, arcSegs, arcRadiusC, arcStart, arcEnd, wireRadius)
wires += gm(deg(0),deg(0),deg(0), c.x, c.y, c.z, arcTag)


# =======================================================================================================
# Write the file
# =======================================================================================================

fileName = 'nec-2m-2el-146.310.nec'
writeCardsToFile(fileName, comments, wires, footer)
copyCardFileToConsole(fileName)


