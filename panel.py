#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: Widget for drawing a raised or sunken panel.
#
#  $RCSfile: panel.py $
#
#   Started$
# $Revision: 1.1 $
#     $Date: 2009/11/15 03:12:14 $
##

from __future__ import print_function
from graphics import *

class Panel:

    # Simply store attributes for later drawing.
    # Corner points stored as lower left and upper right.
    def __init__(self, p1, p2, raised=True, width=5, clrdark="grey50", clrlight="white"):

        # Want lowerleft and upperright corners points.
        x1, x2 = p1.getX(), p2.getX()
        y1, y2 = p1.getY(), p2.getY()
        if (x1>x2) : x1, x2 = x2, x1
        if (y1>y2) : y1, y2 = y2, y1

        self.p1 = p1 = Point(x1,y1)
        self.p2 = p2 = Point(x2,y2)
        self.raised  = raised
        self.clrdark  = clrdark
        self.clrlight = clrlight

        pntulInner = Point(p1.getX()+width, p2.getY()-width)
        pntllInner = Point(p1.getX()+width, p1.getY()+width)
        pntlrInner = Point(p2.getX()-width, p1.getY()+width)
        pnturInner = Point(p2.getX()-width, p2.getY()-width)
        self.rect = Rectangle(pntllInner, pnturInner)

        vertices = []
        vertices.append(p1)
        vertices.append(Point(p2.getX(), p1.getY()))
        vertices.append(p2)
        vertices.append(pnturInner)
        vertices.append(pntlrInner)
        vertices.append(pntllInner)
        vertices.append(p1)
        self.poly1 = Polygon(vertices)

        vertices = []
        vertices.append(p1)
        vertices.append(Point(p1.getX(), p2.getY()))
        vertices.append(p2)
        vertices.append(pnturInner)
        vertices.append(pntulInner)
        vertices.append(pntllInner)
        vertices.append(p1)
        self.poly2 = Polygon(vertices)


    # Panel consists of two irregular polygons, filled in differing shades.
    def draw(self, win):

        colordef = 'black'
        colorfill = self.clrdark if (self.raised) else self.clrlight
        colorout  = colordef     if (self.raised) else colorfill
        self.poly1.setFill( colorfill )
        self.poly1.setOutline( colorout )
        self.poly1.draw(win)

        colorfill = self.clrlight if (self.raised) else self.clrdark
        colorout  = colorfill     if (self.raised) else colordef
        self.poly2.setFill( colorfill )
        self.poly2.setOutline( colorout )
        self.poly2.draw(win)

        self.rect.draw(win)


    # Fill color for inner rectangle of the panel.
    def setFill(self, color):
        self.rect.setFill(color)


    # Fill color for inner rectangle of the panel.
    def setOutline(self, color):
        self.rect.setOutline(color)


    # Return True if passed point within the panel.
    def clicked( self, pnt):
        p1 = self.p1
        p2 = self.p2
        return p1.getX() <= pnt.getX() <= p2.getX() and \
               p1.getY() <= pnt.getY() <= p2.getY()


    # Return corner points.
    def getPanelCorners(self):
        return self.p1, self.p2

    def getInnerCorners(self):
        return self.rect.getP1(), self.rect.getP2()