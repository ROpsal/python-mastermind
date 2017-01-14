#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: A circular button for the MasterMind game.
#
#  $RCSfile: color_button.py $
#
#   Started$
# $Revision: 1.2 $
#     $Date: 2009/11/17 19:29:46 $
##

from __future__ import print_function
from graphics import *

class ColorButton :

    def __init__(self, center, radius, index_color, off_color):

        self.center = center
        self.radius = radius
        self.index_color = index_color
        self.off_color   = off_color

        self.circles = []
        circle = Circle(center, radius)
        circle.setOutline('gray50')
        self.circles.append(circle)

        radius = int(0.94 * radius)
        delta  = self.radius - radius
        center = Point(center.getX() - delta, center.getY() + delta)
        circle = Circle(center, radius)
        circle.setWidth(0)
        self.circles.append(circle)

        self.deactivate()


    # Draw our approximation of a 3D circular button.
    def draw(self, win):
        for circle in self.circles:
            circle.draw(win)


    # Returns True if button active and point within radius.
    def clicked(self, point):
        if (self.active):
            xin = point.getX()
            yin = point.getY()
            xs  = self.center.getX()
            ys  = self.center.getY()
            return (self.radius >= ((xs - xin)**2 + (ys - yin)**2) ** 0.5)
        return False

    # Goes to index color plus active state.
    def activate(self):
        self.circles[0].setWidth(0)
        colors = self.__getColorList()
        for i, circle in enumerate(self.circles):
            circle.setFill(colors[i])
        self.active = True

    def isActive(self):
        return self.active

    # Goes to "off" color plus inactive state.
    def deactivate(self):
        self.circles[0].setWidth(2)
        for circle in self.circles:
            circle.setFill(self.off_color)
        self.active = False

    # Change index color value and activate button.
    def setIndexColor(self, index_color):
        if (None == index_color):
            self.deactivate()
        else:
            self.index_color = index_color
            self.activate()

    # Get the index color value.  None if not active.
    def getIndexColor(self):
        index_color = None
        if (self.active):
            index_color = self.index_color
        return index_color

    # Usually a color that matches the background to "hide" button.
    def setOffColor(self, off_color) :
        self.off_color = off_color
        if (not self.active):
            self.deactivate()


    # Possible list of colors for buttons.
    COLOR_LIST = \
                [   ['red3', 'red2'], 
                    ['orange3', 'dark orange'],
                    ['yellow3', 'yellow2'],
                    ['dark green', 'forest green'],
                    ['RoyalBlue4', 'RoyalBlue2'],
                    ['purple3', 'purple1'],
                    ['VioletRed4', 'medium violet red'],
                    ['snow4', 'snow'],
                    ['black', 'gray25']
                ]

    # List of colors used by the ColorButton class.
    def __getColorList(self):
        return ColorButton.COLOR_LIST[self.index_color % len(ColorButton.COLOR_LIST)]