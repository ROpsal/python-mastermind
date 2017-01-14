#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: Widget for panel style buttons in MasterMind game.
#            "Exit", "Show Me" and "Play" are example buttons.
#
#  $RCSfile: panel_button.py $
#
#   Started$
# $Revision: 1.4 $
#     $Date: 2009/11/17 19:29:46 $
##

from __future__ import print_function
from graphics import *
from panel import Panel

# Panel responsible for panel style buttons in MasterMind game.
class PanelButton(Panel):

    def __init__(self, p1, p2, button_text, raised=True):
        clrBackground = "MistyRose3"

        Panel.__init__(self, p1, p2, raised, 3)
        Panel.setFill(self, clrBackground)
        Panel.setOutline(self, clrBackground)

        center = Point((p1.getX() + p2.getX())//2, (p1.getY() + p2.getY())//2)
        self.text = Text(center, button_text)


    # Draw button outline plus text.
    def draw(self, win):
        self.win = win
        Panel.draw(self, win)
        self.text.draw(win)

    # Set the font for the button.
    def setFace(self, family):
        self.text.setFace(family)

    # Set the size for the font.
    def setSize(self, point):
        self.text.setSize(point)

    # Set the style for the button.
    def setStyle(self, style):
        self.text.setStyle(style)

    # Set the text color for button.
    def setTextColor(self, color):
        self.text.setTextColor( color )

    # Set button text.
    def setText(self, button_text):
        self.text.setText(button_text)
