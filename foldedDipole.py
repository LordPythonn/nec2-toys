'''
Copyright 2012 Will Snook (http://willsnook.com)
MIT License

Use utility functions to generate a NEC2 card stack file for what might be a folded dipole
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
# Make the wire cards
# =======================================================================================================

wireRadius = m(0.001585) # Radius = 1/16", diameter = 1/8"
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

fileName = 'foldedDiPy2.nec'
writeCardsToFile(fileName, comments, wires, footer)
copyCardFileToConsole(fileName)


