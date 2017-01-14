#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: Widget containing MasterMind level and match panels.
#
#  $RCSfile: panel_level.py $
#
#   Started$
# $Revision: 1.3 $
#     $Date: 2009/11/17 19:29:46 $
##

from __future__ import print_function
from graphics import *
from panel import Panel
from color_button import ColorButton

# Panel responsible for level display in MasterMind game.
class PanelLevel(Panel):

    def __init__(self, p1, p2, cntpositions, hideable=False):
        clrBackground = "cornsilk3"
        clrHidden     = "coral2"

        Panel.__init__(self, p1, p2, hideable, 3)
        Panel.setFill(self, clrBackground)
        Panel.setOutline(self, clrBackground)

        p1,p2 = self.getInnerCorners()
        cx = p2.getX() - p1.getX()
        cy = p2.getY() - p1.getY()
        delta  = cx // cntpositions
        radius = delta if (delta < cy) else cy
        radius = int(radius * 0.45)

        centerx = p1.getX() + cx/ cntpositions // 2
        centery = p1.getY() + cy//2

        self.win = None
        self.buttons = []
        for i in range(cntpositions):
            center = Point(centerx + i*delta, centery)
            button = ColorButton(center, radius, 0, clrBackground)
            self.buttons.append(button)

        self.blockview_rect = None
        self.visible = True
        if (hideable):
            p1,p2 = self.getInnerCorners()
            self.blockview_rect = Rectangle(p1, p2)
            self.blockview_rect.setFill(clrHidden)
            self.blockview_rect.setOutline(clrHidden)

    # Draw the panel, buttons, and hider rectangle, if present.
    def draw(self, win):
        self.win = win
        Panel.draw(self, win)
        for button in self.buttons:
            button.draw(win)
        self.hideLevel()

    # Returns index to clicked token; otherwise None value returned.
    def clickedToken(self, pnt):
        token = None
        for i, button in enumerate(self.buttons):
            if button.clicked(pnt):
                token = i
                break
        return token

    # Set the specified token to indicate a selection.
    def setToken(self, colorindex):
        for button in self.buttons:
            if (not button.isActive()):
                button.setIndexColor(colorindex)
                break

    # Clear the specified token, indicating a players change of heart.
    def clearToken(self, token):
        if (0 <= token < len(self.buttons)):
            self.buttons[token].deactivate()

    # Return color indices for this level.
    def getPattern(self):
        pattern = []
        for button in self.buttons:
            pattern.append(button.getIndexColor())
        return pattern

    # Set color indices for this level.
    def setPattern(self, pattern):
        for i,button in enumerate(self.buttons):
            if (i < len(pattern)):
                button.setIndexColor(pattern[i])
            else:
                button.deactivate()

    def showLevel(self):
        if (None != self.win) and (None != self.blockview_rect):
            self.blockview_rect.undraw()
        self.visible = True

    def hideLevel(self):
        if (None != self.win) and (None != self.blockview_rect) and (self.visible):
            self.blockview_rect.draw(self.win)
            self.visible = False


# Panel responsible for match display in MasterMind game.
class PanelMatch(Panel):

    # These are x,y offsets encoded in the integer values.  Two bits for each.
    # This is the reason for the '// 4' and '% 4' operations below.
    COOR = [0,1,2,4,5,6,8,9,10]

    # Patterns for the pips. Origin is lower-left.
    NUMS = [[], [4], [3,5], [1,4,7], [2,8,0,6], [2,8,4,0,6], [2,5,8,0,3,6],
            [2,5,8,4,0,3,6], [2,5,8,1,7,0,3,6], [2,5,8,1,4,7,0,3,6]]

    def __init__(self, p1, p2, cntpositions):
        self.clrBackground = "LavenderBlush3"

        Panel.__init__(self, p1, p2, False, 3)
        Panel.setFill(self, self.clrBackground )
        Panel.setOutline(self, self.clrBackground)

        # Max out the count of positions on bad parameter.
        if (cntpositions >= len(PanelMatch.NUMS)):
            cntpositions =  len(PanelMatch.NUMS)-1

        p1,p2 = self.getInnerCorners()
        frac = 0.15 if (5 >= cntpositions) else 0.125
        radius = int((p2.getX() - p1.getX()) * frac)
        step = (p2.getX() - p1.getX() - 3*radius) // 2

        x0 = p1.getX() + 1.5*radius
        y0 = p1.getY() + 1.5*radius

        self.pips = []
        for num in PanelMatch.NUMS[cntpositions]:
            deltax = int((PanelMatch.COOR[num] // 4) * step)
            deltay = int((PanelMatch.COOR[num]  % 4) * step)
            center = Point(x0+deltax, y0+deltay)
            pip = Circle(center, radius)
            pip.setWidth(1)
            pip.setFill(self.clrBackground)
            pip.setOutline("gray50")
            self.pips.append(pip)


    # Draw the panel, buttons, and hider rectangle, if present.
    def draw(self, win):
        self.win = win
        Panel.draw(self, win)
        for pip in self.pips:
            pip.draw(win)

    # Set the "match" indicator area.
    def setMatches(self, blacks, whites):
        for pip in self.pips:
            if (blacks):
                pip.setFill('black')
                blacks -= 1
            elif (whites):
                pip.setFill('white')
                whites -= 1
            else:
                pip.setFill(self.clrBackground)