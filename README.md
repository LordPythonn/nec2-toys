nec2-toys
=========

Python functions to help model antennas in xnec2c by generating nec2 card stack files


Background
----------

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
of an understatement. I make no claims of expertise here. My goal is just to
bring the process of feeding geometry to xnec2c down into the realm of what's
at least moderately practical for me to comprehend and modify.

Ultimately I hope to answer the question, can expect the 2m/70cm Cheap Yagi
designs which Kent published for satallite uplink and downlink work to also
function at reasonable efficiency with repeaters elsewhere on the 2m and 70cm
Amateur bands?


Background information and documentation on nec2...
* http://en.wikipedia.org/wiki/Numerical_Electromagnetics_Code
* http://www.nec2.org/
* http://www.qsl.net/5b4az/pages/nec2.html
* http://www.wa5vjb.com/about.html


License
-------

I'm releasing this project under the MIT license, a copy of which is included in
the LICENSE file.


Author & Copyright
------------------

Copyright (c) 2012 Will Snook (http://willsnook.com)
