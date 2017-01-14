#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: Widget containing the MasterMind game panel levels and matches.
#
#  $RCSfile: panel_game.py $
#
#   Started$
# $Revision: 1.3 $
#     $Date: 2009/11/17 03:13:04 $
##

from __future__ import print_function
from graphics import *
from panel import Panel
from panel_level import PanelLevel, PanelMatch

# Panel responsible for displaying levels within the MasterMind game.
# Last level is for viewing the solution.
class PanelGame(Panel):

    def __init__(self, p1, p2, cntlevels, cntpositions):
        clrBackground = "light coral"

        Panel.__init__(self, p1, p2, True, 5)
        Panel.setFill(self, clrBackground)
        Panel.setOutline(self, clrBackground)

        p1,p2 = self.getInnerCorners()
        cx = p2.getX() - p1.getX()
        cy = p2.getY() - p1.getY()
        deltay = cy // cntlevels

        height_level = width_match = height_match = int(deltay * 0.90)
        margin = cy - height_level*cntlevels
        margin //= cntlevels + 1
        width_level = cx - width_match - 3*margin

        x2 = p2.getX() - margin
        y2 = p2.getY() - margin
        x1 = x2 - width_match
        y1 = y2 - height_match

        self.matches = []
        for i in range(cntlevels-1):
            pll = Point(x1, y1 - i * deltay)
            pur = Point(x2, y2 - i * deltay)
            match = PanelMatch(pll, pur, cntpositions)
            self.matches.append(match)

        x2 = p2.getX() - 2 * margin - width_match
        y2 = p2.getY() - margin
        x1 = x2 - width_level
        y1 = y2 - height_level

        self.levels = []
        for i in range(cntlevels):
            pll = Point(x1, y1 - i * deltay)
            pur = Point(x2, y2 - i * deltay)
            level = PanelLevel(pll, pur, cntpositions, (i == cntlevels-1))
            self.levels.append(level)

    # Draw the level and match panels.
    def draw(self, win):
        self.win = win
        Panel.draw(self, win)
        for match in self.matches:
            match.draw(win)
        for level in self.levels:
            level.draw(win)

    # Returns indices to level and token; otherwise None values returned.
    def clickedLevel(self, pnt):
        ident = token = None
        for i, level in enumerate(self.levels):
            if level.clicked(pnt):
                ident = i
                token = level.clickedToken(pnt)
                break
        return ident,token

    # Set the specified token to indicate a selection.
    def setToken(self, ident, colorindex):
        if (0 <= ident < len(self.levels)):
            self.levels[ident].setToken(colorindex)

    # Clear the specified token, indicating a players change of heart.
    def clearToken(self, ident, token):
        if (0 <= ident < len(self.levels)):
            self.levels[ident].clearToken(token)

    # Set the "match" indicator area.
    def setMatches(self, ident, blacks, whites):
        if (0 <= ident < len(self.matches)):
            self.matches[ident].setMatches(blacks, whites)

    # Configure pattern for the specified level.
    def setPattern(self, ident, pattern):
        if (0 <= ident < len(self.levels)):
            self.levels[ident].setPattern(pattern)

    # Retrieve pattern for the specified level.
    def getPattern(self, ident):
        pattern = []
        if (0 <= ident < len(self.levels)):
            pattern = self.levels[ident].getPattern()
        return pattern

    # Get the MasterMind solution pattern.
    def getSolutionPattern(self):
        level = self.levels[-1]
        return level.getPattern()

    # Set the MasterMind solution pattern.
    def setSolutionPattern(self, pattern):
        level = self.levels[-1]
        level.setPattern(pattern)

    # Show the MasterMind solution pattern.
    def showSolutionPattern(self):
        level = self.levels[-1]
        level.showLevel()

    # Hide the MasterMind solution pattern.
    def hideSolutionPattern(self):
        level = self.levels[-1]
        level.hideLevel()