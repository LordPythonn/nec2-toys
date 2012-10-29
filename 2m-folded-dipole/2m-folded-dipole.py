'''
Copyright 2012 Will Snook (http://willsnook.com)
MIT License

Generate a NEC2 card stack file for a 2m folded dipole
'''

from nec2utils import *


# =======================================================================================================
# Plan for a 2m folded dipole
# =======================================================================================================

'''
Notes:
  '+' marks a boundary between wire elements
  'X' marks the feedpoint
  Material is 1/8" diameter bare copper wire
  Total length of wire is 1 wavelength of center frequency
  Wavelength = (300 * velocity factor of 1/8" bare copper) / (design frequency)
  A = (1/2 wavelength) - (pi * rb)

        a1                                   A                                   a2 
     ,-+---------------------------------------------------------------------------+-,
    /                                                                                 \
 D |rd d                                                                           b rb| B
    \                                                                                 /
     `-+-------------------------------------X-------------------------------------+-'
        c2                                   C                                   c1

'''

targetMHz        = 146.310
correctionFactor = 0.932   # Trial and error correcion constant to account for velocity factor, etc
wavelength       = m((300.0 * correctionFactor) / targetMHz)

radiusB = inch(0.5)
radiusD = radiusB
A       = (0.5 * wavelength) - (math.pi*radiusB)
C       = A
Y0      = inch(5.0 + (2.0/8.0))
Z0      = inch(36.0)

comments  = 'CM -------------------------------------------------------------------\n'
comments += 'CM  NEC2 model for simulating a folded dipole built from copper wire.\n'
comments += 'CM  Geometry is tuned for min SWR at {:.3f} MHz\n'.format(targetMHz)
comments += 'CM  \n'
comments += 'CM  Wire length before bends = {: >6.3f} in\n'.format(mToIn(wavelength))
comments += 'CM  Radius of bends          = {: >6.3f} in\n'.format(mToIn(radiusB))
comments += 'CM -------------------------------------------------------------------\n'
comments += 'CE'

a1 = Point(A/2.0, Y0, Z0)
a2 = Point(-a1.x, Y0, Z0)
b  = Point( a2.x, Y0, Z0-radiusB)
c1 = Point( a2.x, Y0, Z0-(2.0*radiusB))
c2 = Point( a1.x, Y0, c1.z)
d  = Point( a1.x, Y0, b.z)

wireRadius = inch(1.0/16.0) # radius for a 1/8" wire
segs       = 51
arcSegs    = 15
arcStart   = deg(90)
arcEnd     = deg(270)

m = Model(wireRadius)
m.addWire(segs, a1, a2)
m.addArc(arcSegs, radiusB, arcStart, arcEnd, rotate=Rotation(deg(0),deg(0),deg(0)), translate=b)
m.addWire(segs, c1, c2).feedAtMiddle()
m.addArc(arcSegs, radiusD, arcStart, arcEnd, rotate=Rotation(deg(0),deg(0),deg(180)), translate=d)

steps = (148.0 - 144.0) / 0.1
cardStack = m.getText(start=144.000, stepSize=0.1, stepCount=steps)


# =======================================================================================================
# Write the file
# =======================================================================================================

fileName = '2m-folded-dipole.nec'
writeCardsToFile(fileName, comments, cardStack)
copyCardFileToConsole(fileName)


