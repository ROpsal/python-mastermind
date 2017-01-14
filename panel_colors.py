#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: Widget containing the MasterMind game color panel.
#
#  $RCSfile: panel_colors.py $
#
#   Started$
# $Revision: 1.2 $
#     $Date: 2009/11/17 19:29:46 $
##

from __future__ import print_function
from graphics import *
from panel import Panel
from color_button import ColorButton

# Panel responsible for color selection in MasterMind game.
class PanelColors(Panel):

    def __init__(self, p1, p2, cntcolors):
        clrBackground = "PeachPuff2"

        Panel.__init__(self, p1, p2, True, 5)
        Panel.setFill(self, clrBackground )
        Panel.setOutline(self, clrBackground)

        p1,p2 = self.getInnerCorners()
        cx = p2.getX() - p1.getX()
        cy = p2.getY() - p1.getY()
        delta  = cy // cntcolors
        radius = delta if (delta < cx) else cx
        radius = int(radius * 0.40)

        centerx = p1.getX() + cx// 2
        centery = p1.getY() + cy/ cntcolors // 2

        self.win = None
        self.buttons = []
        for i in range(cntcolors):
            center = Point(centerx, centery+ (cntcolors -1 -i)*delta)
            button = ColorButton(center, radius, i, clrBackground)
            button.activate()
            self.buttons.append(button)


    # Draw the panel, buttons, and hider rectangle, if present.
    def draw(self, win):
        self.win = win
        Panel.draw(self, win)
        for button in self.buttons:
            button.draw(win)

    # Returns indices to level and token; otherwise None values returned.
    def clickedColor(self, pnt):
        colorid = None
        for i, button in enumerate(self.buttons):
            if button.clicked(pnt):
                colorid = i
                break
        return colorid