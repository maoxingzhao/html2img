#!/usr/bin/python
#
#   Copyright (c) 2010. Piotr Mitros.  This program is free software:
#    you can redistribute it and/or modify it under the terms of the
#    GNU General Public License, version 2 of the License, GNU Lesser
#    General Public License version 3 of the License, or (at your
#    option) any later versions of either license, as published by the
#    Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


from PySide.QtWebKit import *
from PySide import QtGui, QtCore
import sys, bisect, getopt

app=QtGui.QApplication([])

page=QWebPage()

settings={'url' : 'http://www.google.com/',
        'output' : 'tmp.png',
        'height' : '400', 
        'width' :  '400',
        'xscale' : 'True', 
        'yscale' : 'True',
        'maxheight' : '16384',
        'maxwidth' : '4096', 
        'minheight' : '1',
        'minwidth' : '1', 
        'timeout' : '10.0'}

option_strings=[option+'=' for option in settings]

def usage():
    print "Usage:"
    print "  html2img1 --url=http://web.mit.edu --output=mit.png"
    print
    print "Major options:"
    print "  --url=LOCATION"
    print "  --output=filename"
    print
    print "html2img1 has two ways of picking image size. By default"
    print "it will pick the smallest image that will fit the web "
    print "page, with bounds set by minwidth, maxwidth, minheight, "
    print "and maxheight. Alternatively, you can specify a width and "
    print "height. The specific algorithm is: " 
    print "  Assume width=width, height=height. If xscale is true, scale "
    print "  the width until there is no horizontal scrollbar necessary. "
    print "  if yscale is true, scale the height until there is no"
    print "  vertical scrollbar necessary."
    print "Parameters:"
    print "  --height=NNN (default 400)"
    print "  --width=NNN (default 400)"
    print "  --minwidth=NNN (default 1)"
    print "  --maxwidth=NNN (default 4096)"
    print "  --minheight=NNN (default 1)"
    print "  --maxheight=NNN (default 16384)"
    print "  --xscale=true/[anything else]"
    print "  --yscale=true/[anything else]"
    print
    print "Known Bugs: Requires X"
    sys.exit(0)

try: 
    opts, args = getopt.getopt(sys.argv[1:], "", option_strings)
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)

for (name,value) in opts:
    settings[name[2:]]=value

#print settings

height=int(settings['height'])
width=int(settings['width'])
maxheight=int(settings['maxheight'])
maxwidth=int(settings['maxwidth'])
minheight=int(settings['minheight'])
minwidth=int(settings['minwidth'])
xscale=settings['xscale'].lower()=='true'
yscale=settings['yscale'].lower()=='true'
output=settings['output']
url=settings['url']
timeout=float(settings['timeout'])
#=settings[''])


page.setViewportSize(QtCore.QSize(width,height))
frame=page.mainFrame()

def callback(bool):
    global height, width

    if xscale:
        class lazy_list:
            def __getitem__(self, key):
                page.setViewportSize(QtCore.QSize(key, height))
                return not frame.scrollBarMaximum(QtCore.Qt.Horizontal)!=0

        width=bisect.bisect(lazy_list(), 0.5, minwidth, maxwidth)

    if yscale:
        class lazy_list:
            def __getitem__(self, key):
                page.setViewportSize(QtCore.QSize(width,key))
                return not frame.scrollBarMaximum(QtCore.Qt.Vertical)!=0

        height=bisect.bisect(lazy_list(), 0.5, minheight, maxheight)

    pm=QtGui.QPixmap(width, height)
    painter=QtGui.QPainter()
    painter.begin(pm)
    frame.render(painter)
    painter.end()
    pm.save(output)
    print height,width
    sys.exit()

frame.connect(frame, QtCore.SIGNAL('loadFinished(bool)'), callback)
frame.load(QtCore.QUrl(url))

app.exec_()


