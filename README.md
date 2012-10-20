nec2-toys
=========

Python-assisted nec2 antenna modeling for tuning the "Cheap Yagi" design


The Nec2 Antenna Modelling Part
-------------------------------

The point of this project is to generate nec2 card stack files to help with
antenna modeling.  I'm using this with xnec2c in Linux, but in theory it may
work on other platforms with some of the various nec2 based antenna modeling
programs.  The particular antennas I'm interested in are variants of the "Cheap
Yagi" design by Kent Britain, WA5VJB.

The Numerical Electromagnetics Code software originated at Lawrence Livermore
Labs in the 1970's. It started in FORTRAN then was eventually translated to C.
Current nec2 based modeling programs still revolve around an input format which
is closely based on what was used with FORTRAN punch cards back in the day.

Describing the process of modeling antennas with nec2 as arcane would be a bit
of an understatement. I make no claims of expertise here.

Nec2 links:
* http://en.wikipedia.org/wiki/Numerical_Electromagnetics_Code
* http://www.nec2.org/
* http://www.qsl.net/5b4az/pages/nec2.html


The Cheap Yagi Part
-------------------

I'm doing this because I want to figure out if I can expect the 2m/70cm Cheap
Yagi designs which Kent published for satellite uplink and downlink work to
also function at reasonable efficiency with repeaters elsewhere on the 2m and
70cm Amateur bands.

Link to pdfs about Kent Britain's Cheap Yagi Designs:
* http://www.wa5vjb.com/references.html


Usage
-----

Running nec2utils.py directly won't accomplish much as it contains utilty
functions which meant to be used by the model generators.

The model generators, like `drivenElement.py` and `2m-2el-1_8th-yagi.py`, are
meant to be run with python from the console. At the moment the generators each
include a hardcoded output file name to which they write a nec2 formatted card
stack. For example, 

`$ python drivenElement.py`

will write the card stack for the driven element of a 2m Yagi to the file
`freeSpace2mDE.nec` in the current working directory. It will also read the file
back out to the console for a quick sanity check.

To generate plots or other output, you need to feed the .nec files to a nec2
based antenna modelling program. I use xnec2c on Linux, but there are plenty of
other options which should theoretically work too.


License
-------

I'm releasing this project under the MIT license, a copy of which is included
in the LICENSE file. Note that the Cheap Yagi design itself is Kent Britain's,
not mine.


Author & Copyright
------------------

Copyright (c) 2012 Will Snook (http://willsnook.com)
