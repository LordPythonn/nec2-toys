'''
Copyright 2012 Will Snook (http://willsnook.com)
MIT License

Generate a NEC2 card stack file for a 2m yagi fed with a folded dipole driven element
'''

from nec2utils import *


# =======================================================================================================
# Plan for a 2m yagi fed with folded dipole
# =======================================================================================================

'''
Notes:
  '+' marks a boundary between wire elements
  'X' marks the feedpoint
  Material is 1/8" diameter bare copper wire
  Total length of wire is 1 wavelength of center frequency
  Wavelength = (300 * velocity factor of 1/8" bare copper) / (design frequency)
  A = (1/2 wavelength) - (pi * rb)


# Driven Element:

        a1                                   A                                   a2 
     ,-+---------------------------------------------------------------------------+-,
    /                                                                                 \
 D |rd d                                                                           b rb| B
    \                                                                                 /
     `-+-------------------------------------X-------------------------------------+-'
        c2                                   C                                   c1


# Reflector:

    e1                                       E                                       e2
    -----------------------------------------------------------------------------------

'''

targetMHz        = 146.310
#correctionFactor = 0.932   # Trial and error correcion constant to account for velocity factor, etc
correctionFactor = 0.9347   # Trial and error correcion constant to account for velocity factor, etc
wavelength       = m((300.0 * correctionFactor) / targetMHz)

# Folded dipole driven element
radiusB = inch(1.0)
radiusD = radiusB
A       = (0.5 * wavelength) - (math.pi*radiusB)
C       = A
#Y0      = inch(5.0 + (2.0/8.0))
Y0      = inch(5.0 + (3.0/8.0))
Z0      = inch(36.0)

# Reflector
Y1 = inch(0)
E  = inch(40.0 + (2.0/8.0))


comments  = 'CM -------------------------------------------------------------------\n'
comments += 'CM  NEC2 model for simulating a folded dipole built from copper wire.\n'
comments += 'CM  Geometry is tuned for min SWR at {:.3f} MHz\n'.format(targetMHz)
comments += 'CM  \n'
comments += 'CM  Wire length before bends = {: >6.3f} in\n'.format(mToIn(wavelength))
comments += 'CM  Radius of bends          = {: >6.3f} in\n'.format(mToIn(radiusB))
comments += 'CM -------------------------------------------------------------------\n'
comments += 'CE'

# DE
a1 = Point(A/2.0, Y0, Z0)
a2 = Point(-a1.x, Y0, Z0)
b  = Point( a2.x, Y0, Z0-radiusB)
c1 = Point( a2.x, Y0, Z0-(2.0*radiusB))
c2 = Point( a1.x, Y0, c1.z)
d  = Point( a1.x, Y0, b.z)
# Ref
e1 = Point( E/2.0, Y1, b.z)
e2 = Point(-E/2.0, Y1, b.z)

wireRadius = inch(1.0/16.0) # radius for a 1/8" wire
segs       = 41
arcSegs    = 15
arcStart   = deg(90)
arcEnd     = deg(270)

m = Model(wireRadius)
# Driven element
m.addWire(segs, a1, a2)
m.addArc(arcSegs, radiusB, start=deg(90), end=deg(270), rotate=Rotation(deg(0),deg(0),deg(0)), translate=b)
m.addWire(segs, c1, c2).feedAtMiddle()
m.addArc(arcSegs, radiusD, arcStart, arcEnd, rotate=Rotation(deg(0),deg(0),deg(180)), translate=d)
# Reflector
m.addWire(segs, e1, e2)

steps = (147.5 - 145.5) / 0.05
cardStack = m.getText(start=145.500, stepSize=0.05, stepCount=steps)


# =======================================================================================================
# Write the file
# =======================================================================================================

fileName = '2m-fd-fed-yagi.nec'
writeCardsToFile(fileName, comments, cardStack)
copyCardFileToConsole(fileName)


