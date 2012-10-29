'''
Copyright 2012 Will Snook (http://willsnook.com)
MIT License

Generate a NEC2 card stack file for a 2m folded dipole
'''

from nec2utils import *


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
refLength           = inch(40.0 + (2.0/8.0))

targetMHz           = 146.310
velocityFactor      = 0.937   # This is what seems to work from trial and error simulations with 1/8" wires
quarterWavelength   = m((300.0 * 0.937) / targetMHz) / 4.0 
arcRadiusC          = inch(0.25)
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

a1   = Point(quarterWavelength, deY, deTopZ)
a2   = Point(0.0, deY, deTopZ)
b1   = a2
b2   = Point(-bLength, b1.y, b1.z)
c    = Point(b2.x, deY, deTopZ-arcRadiusC)
d1   = Point(b2.x, deY, deTopZ-(2.0*arcRadiusC))
d2   = Point(a2.x, deY, d1.z)
e1   = d2
e2   = a2


wireRadius = inch(1.0/16.0) # radius for a 1/8" wire
segs = 25
refSegs = 51
arcSegs = 15
arcStart = deg(90)
arcEnd   = deg(270)
feedpointSegs = 1           # My reading of the EZNEC's feed point docs suggests this is how to attach coax

m = Model(wireRadius)

# Driven element
m.addWire(segs, a1, a2)
m.addWire(segs, b1, b2)
m.addArc(arcSegs, arcRadiusC, arcStart, arcEnd, rotate=Rotation(deg(0),deg(0),deg(0)), translate=c)
m.addWire(segs, d1, d2)
m.addWire(feedpointSegs, e1, e2).attachToEX()

cardStack = m.getText(start=145.710, stepSize=0.05, stepCount=30)



# =======================================================================================================
# Write the file
# =======================================================================================================

fileName = '2m-folded-dipole.nec'
writeCardsToFile(fileName, comments, cardStack, "")
copyCardFileToConsole(fileName)


