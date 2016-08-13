html2img
========

html2img is a small python script for grabbing web pages as
images. To grab web.mit.edu, at a natural size for the page:

    html2img1.py --url=http://web.mit.edu --output=mit.png
To grab Mission Motors web page, forcing height to 1024: 

html2img1.py --url="http://www.ridemission.com" --output="emission.png" --yscale=false --height=1024

Requirements:

* Python
* PyQt4 (presumably, once it is PySide will be a better alternative).

Usage details
-------------

Main options:

    --url=LOCATION
    --output=filename

html2img has two ways of picking image size. By default
it will pick the smallest image that will fit the web 
page, with bounds set by minwidth, maxwidth, minheight, 
and maxheight. Alternatively, you can specify a width and 
height. The specific algorithm is: 

*Assume width=width, height=height. If xscale is true, scale
the width until there is no horizontal scrollbar necessary. 
if yscale is true, scale the height until there is no
vertical scrollbar necessary.*

Parameters:

    --height=NNN (default 400)
    --width=NNN (default 400)
    --minwidth=NNN (default 1)
    --maxwidth=NNN (default 4096)
    --minheight=NNN (default 1)
    --maxheight=NNN (default 16384)
    --xscale=true/[anything else]
    --yscale=true/[anything else]

For some pages, you may need to mess with this a little bit --
there isn't always a natural resolution.

Known Bugs
----------

* Requires X
* Doesn't time out nicely if pages cannot load. 

Unknown Bugs
------------

Many! The code is relatively untested. I use it occasionally, but I
certainly haven't hit on each corner case.

License
-------

Copyright (c) 2010. Piotr Mitros. May be distributed under GPLv2.0 or
later, or LGPLv3.0 or later.
