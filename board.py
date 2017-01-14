#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: The "view", also known as the MasterMind board.
#            This is the primary user interface widget.
#
#  $RCSfile: board.py $
#
#   Started$
# $Revision: 1.5 $
#     $Date: 2009/12/01 18:02:23 $
##

from __future__ import print_function
from graphics import *
from panel_game import PanelGame
from panel_colors import PanelColors
from panel_button import PanelButton


# Return a reasonable button height.
def _heightOfButton() :
    return 40

# Return a reasonable margin width.
def _widthOfMargin() :
    return 8

# Return a reasonable width for color panel.
def _widthOfColorPanel() :
    return 120

# Calculate a reasonable game panel height.
def _heightOfGamePanel(sizey):
    return sizey - 2 * _widthOfMargin()

# Calculate a reasonable game panel width.
def _widthOfGamePanel(sizey, cntlevels, cntpositions):
    cylevel = sizey * 0.90 / cntlevels
    cxmatch = cylevel * 2
    cxpanel = cylevel * cntpositions + cxmatch + 3 * _widthOfMargin()
    cxpanel = int(cxpanel + 0.5)
    return cxpanel

# Calculate a reasonable board width.
def _widthOfBoard(sizey, cntlevels, cntpositions):
    sizex = _widthOfGamePanel(sizey, cntlevels, cntpositions) + \
            _widthOfColorPanel() + 3 * _widthOfMargin()
    return int(sizex + 0.5)

# Determine the corner points for the game panel.
def _cornersOfGamePanel( sizex, sizey, cx, cy ):
    ymargin = (sizey - cy) / 2
    x1 = sizex - cx - _widthOfMargin()
    y1 = ymargin
    x2 = sizex - _widthOfMargin()
    y2 = cy + ymargin
    return Point(x1, y1), Point(x2, y2)

# Determine the corner points for the color panel.
def _cornersOfColorPanel( sizey, cntcolors):
    x1 = y1 = _widthOfMargin()
    x2 = x1 + _widthOfColorPanel()
    height = cntcolors * _widthOfColorPanel() * 0.7
    y2 = y1 + height
    if (y2 < sizey  //2): y2 = sizey//2
    if (y2 > sizey*3//4): y2 = sizey*5//8
    return Point(x1, y1), Point(x2, y2)

# Determine the corner points for the exit button.
def _cornersOfExitButton( sizey ):
    x1 = _widthOfMargin()
    x2 = x1 + _widthOfColorPanel()
    y2 = sizey - _widthOfMargin()
    y1 = y2 - _heightOfButton()
    return Point(x1, y1), Point(x2, y2)

# Determine the corner points for the action.
def _cornersOfActionButton( sizey, cntcolors):
    p1,p2 = _cornersOfColorPanel( sizey, cntcolors )
    x1 = p1.getX()
    x2 = p2.getX()
    y1 = p2.getY() + _widthOfMargin()
    y2 = y1 + _heightOfButton()
    return Point(x1, y1), Point(x2, y2)

# Determine corners for message area.
def _cornersOfMessageArea( sizey, cntcolors):
    eb1,eb2 = _cornersOfExitButton( sizey )
    ab1,ab2 = _cornersOfActionButton( sizey, cntcolors )
    x1 = ab1.getX()
    x2 = ab2.getX()
    y1 = ab2.getY() + 2*_widthOfMargin()
    y2 = eb1.getY() - 2*_widthOfMargin()
    return Point(x1, y1), Point(x2, y2)

# Representation of the MasterMind board.
class Board:

    # The graphical divisions of the MasterMind board
    BUTTON_EXIT, BUTTON_ACTION, PANEL_COLORS, PANEL_GAME = range(0, 4)

    # Object initialization.
    def __init__( self, sizey, cntcolors=6, cntlevels=10, cntpositions=4 ):
        self.win = None
        self.sizex = _widthOfBoard( sizey, cntlevels, cntpositions )
        self.sizey = sizey

        self.cntcolors = cntcolors
        self.cntlevels = cntlevels
        self.cntpositions = cntpositions

        cx = _widthOfGamePanel( sizey, cntlevels, cntpositions )
        cy = _heightOfGamePanel( sizey )
        p1, p2 = _cornersOfGamePanel( self.sizex, sizey, cx, cy)
        self.panelGame = PanelGame(p1, p2, cntlevels, cntpositions)

        p1, p2 = _cornersOfColorPanel( sizey, cntcolors )
        self.panelColors = PanelColors( p1, p2, cntcolors )

        p1, p2 = _cornersOfExitButton( sizey )
        self.btnExit = PanelButton( p1, p2, "Exit" )
        self.btnExit.setTextColor( 'red2' )
        self.btnExit.setStyle( 'bold' )
        self.btnExit.setSize(20)

        p1, p2 = _cornersOfActionButton( sizey, cntcolors )
        self.btnAction = PanelButton( p1, p2, "Action" )
        self.btnAction.setTextColor( 'RoyalBlue3' )
        self.btnAction.setStyle( 'bold' )
        self.btnAction.setSize(12)

        p1, p2 = _cornersOfMessageArea( sizey, cntcolors )
        self.panelMsg = PanelButton( p1, p2, "", False )
        self.panelMsg.setTextColor( 'coral3' )
        self.panelMsg.setStyle( 'bold' )
        self.panelMsg.setSize(12)
        self.panelMsg.setFill('antique white')

        self.panels = [self.btnExit, self.btnAction, self.panelColors, self.panelGame]
        self.sections = [Board.BUTTON_EXIT, Board.BUTTON_ACTION, Board.PANEL_COLORS, Board.PANEL_GAME]

    # Python's destructor mechanism.
    # Note: This doesn't seem to work when called from Python IDE's.
    def __del__(self):
        if ( None != self.win):
            self.win.close()

    # Manual closing of the graphics.py "win" object.
    def close(self):
        if ( None != self.win):
            self.win.close()
            self.win = None

    # Draw the MasterMind board.
    def draw(self):
        if (None == self.win):
            self.win = GraphWin( "Ultimate MasterMind", self.sizex, self.sizey )
            self.win.setCoords( 0, 0, self.sizex, self.sizey )
            self.win.setBackground( "cornsilk2" )

        for panel in self.panels:
            panel.draw(self.win)

        self.panelMsg.draw(self.win)
        self.reset()

    # Reset board back to initial conditions.
    def reset(self):
        for id in range(self.cntlevels):
            self.clearMatches(id)
            self.setPattern(id, [])
        self.hideSolutionPattern()

    # Returns one of the graphical area enumerations or None if no hit.
    def clicked(self, pnt):
        section = None
        for i, panel in enumerate(self.panels):
            if panel.clicked(pnt):
                section = self.sections[i]
                break
        return section

    # Returns an index to selected color or None if no hit.
    def clickedColor(self, pnt):
        return self.panelColors.clickedColor(pnt)

    # Returns indices to level and token; otherwise None values returned.
    def clickedLevel(self, pnt):
        return self.panelGame.clickedLevel(pnt)

    # Set the specified token to indicate a selection.
    def setToken(self, ident, colorindex):
        self.panelGame.setToken(ident, colorindex)

    # Clear the specified token, indicating a players change of heart.
    def clearToken(self, ident, token):
        self.panelGame.clearToken(ident, token)

    # Set the "match" indicator area.
    def setMatches(self, ident, blacks, whites):
        self.panelGame.setMatches(ident, blacks, whites)

    # Set the "match" indicator area.
    def clearMatches(self, ident):
        self.panelGame.setMatches(ident, 0, 0)

    # Retrieve pattern for the specified level.
    def setPattern(self, ident, pattern):
        self.panelGame.setPattern(ident, pattern)

    # Retrieve pattern for the specified level.
    def getPattern(self, ident):
        return self.panelGame.getPattern(ident)

    # Get the MasterMind solution pattern.
    def getSolutionPattern(self):
        return self.panelGame.getSolutionPattern()

    # Set the MasterMind solution pattern.  Color indices passed in as a list.
    def setSolutionPattern(self, pattern):
        self.panelGame.setSolutionPattern(pattern)

    # Show the MasterMind solution pattern.
    def showSolutionPattern(self):
        self.panelGame.showSolutionPattern()

    # Hide the MasterMind solution pattern.
    def hideSolutionPattern(self):
        self.panelGame.hideSolutionPattern()

    # All user interactions happen via the mouse.
    def getMouse(self) :
        if (None != self.win):
            return self.win.getMouse()
        else:
            return Point()

    # Board configuration information.
    def getColorCount(self) :
        return self.cntcolors

    def getLevelCount(self):
        return self.cntlevels

    def getPositionCount(self):
        return self.cntpositions

    # Action button has changeable text.
    def setActionButtonText(self, text):
        self.btnAction.setText(text)

    # Message panel has changeable text.
    def setMessagePanelText(self, text):
        self.panelMsg.setText(text)