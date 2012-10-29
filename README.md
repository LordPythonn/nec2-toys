nec2-toys
=========

Experiments in Python-assisted nec2 antenna modeling


Goals, History, and Current Status
----------------------------------

I started this project because I wanted to modify Kent Britain's "Cheap Yagi"
designs to work with a local repeater. Kent's published 2m Yagi designs are
tuned for use near 145 MHz with a relatively narrow usable transmit bandwidth.
Since I wanted an antenna for transmitting between 146 and 147 MHz, my initial
goal was to model Kent's designs and then adjust them to work at a higher
frequency range. That goal has now expanded to include experimenting with other
types of antennas.

Before I started this project, I was manually entering geometry into the xnec2c
modeling software for linux. That quickly grew too complicated to continue
experimenting with in a reasonable manner, so I began using Python to generate
nec2 format antenna model files. My Python code abstracts away many of the
details of the arcane nec2 card stack file format, so it's now much easier for
me to iterate through many changes in antenna geometry.

My new workflow is to specify geometry in terms of variables and formulas in
python, run my code to translate that into an antenna model in the nec2 file
format, then open the .nec file in xnec2c to simulate the model's performance.
So far this has been working reasonably well.

I'm gradually building more intelligence about nec2 into my utility code so
that I can write model generators for more complicated antennas which are
increasingly free of arcane nec2-related clutter. My first generation model
generators included blocks of hardcoded nec2 format text, a good abstraction
system for generating straight wires, and a functional but ugly kludge
for modeling a single circular wire arc (good enough for my initial
prototypes).

Since I now want to experiment with folded dipoles, which require two wire
arcs, I've started a second generation of my utility code as`/nec2utils.py`. I
moved the first generation utility code into `oldStuff/gen1/` along with the
related model generator scripts. For the moment I want to keep those
designs around as a reference.

In addition to a good abstraction for multiple circular arcs, my second
generation utility code is smart enough to generate GE, FR, EX, RP, and EN
cards. Those changes mean my model generators can now communicate various
high-level intentions in small amounts of python code rather than lots of
obscure hard-coded nec2 text blocks.


Nec2 Antenna Modelling
----------------------

The Numerical Electromagnetics Code antenna modeling software originated at
Lawrence Livermore Labs in the 1970's. It started in FORTRAN and was later
translated to C.  Currently there are many nec2 based modeling programs, some
text based, and some with fancy GUI's. However, they still revolve around an
input format which is closely based on what was used with the original FORTRAN
punch cards (see http://www.nec2.org/)


Usage
-----

My utility code for dealing with the messy details of nec2 is located in
`nec2utils.py`. It is meant to be imported by the generator scripts for
individual antenna models.

Model generators, say `antenna1.py` or `antenna2.py`, are
meant to be run with python from the console. At the moment the generators each
include a hardcoded output filename to which they write a nec2 formatted card
stack. For example, running

`$ python antenna1.py`

might write antenna geometry to the file `antenna1.nec` in the current working
directory. My generator scripts so far also read the file back out to the
console for a quick sanity check.

To make plots or other output, you need to feed the .nec files to a nec2
based antenna modeling program. I use xnec2c on Linux, but there are plenty of
other options which should theoretically work too.


License
-------

I'm releasing this project under the MIT license, a copy of which is included
in the LICENSE file.

Credits
-------

The Cheap Yagi design was originated by Kent Britain, http://www.wa5vjb.com/references.html


Author & Copyright
------------------

Copyright (c) 2012 Will Snook (http://willsnook.com)
