nec2-toys
=========

Python-assisted nec2 antenna modeling for tuning the "Cheap Yagi" design


The Cheap Yagi Antenna Design
-----------------------------

I'm doing this because I want to modify Kent Britain's 2m/70cm Cheap Yagi
designs (see http://www.wa5vjb.com/references.html). Kent's published
measurements are tuned for use on amateur radio satellite uplink and downlink
frequencies.  I would like to optimize his design for use with repeaters and
transmitter hunting in other portions of the 2m and 70cm Amateur bands. I'm
using this code to generate .nec antenna geometry files for use with a nec2
based antenna modelling progam (xnec2c on Linux).


Nec2 Antenna Modelling
----------------------

The Numerical Electromagnetics Code antenna modelling software originated at
Lawrence Livermore Labs in the 1970's. It started in FORTRAN and was later
translated to C.  Currently there are many nec2 based modeling programs, some
text based, and some with fancy GUI's. However, they still revolve around an
input format which is closely based on what was used with the original FORTRAN
punch cards (see http://www.nec2.org/)

My experience with attempting to manually edit antenna geometry was painful. I
wanted to use named variables for measurements, unit conversion functions,
ASCII art sketches, etc. Now that I'm doing the heavy lifting in Python, life
is good. The utility functions handle the arcane and repetitive parts of nec2's
syntax, and I get to focus on the geometry.  This way it's actually almost fun to
adjust and experiment.  There are still some important things that I need to
parameterize, like the FR and EX cards.


Usage
-----

Running `nec2utils.py` directly won't accomplish much as it contains utilty
functions which are meant to be imported by the model generators.

The model generators, like `drivenElement.py` and `2m-2el-1_8th-yagi.py`, are
meant to be run with python from the console. At the moment the generators each
include a hardcoded output filename to which they write a nec2 formatted card
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
