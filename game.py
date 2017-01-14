#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: The "model", also known as the MasterMind game logic.
#
#  $RCSfile: game.py $
#
#   Started$
# $Revision: 1.4 $
#     $Date: 2009/12/01 18:02:23 $
##

from __future__ import print_function
from random import randint, choice
from board import Board

# Message to display when exiting game.
def _gameExitMessage(fWonGame, ident, cntlevels):
    message = "Better\nLuck\nNext Time"
    if (fWonGame):
        if   ( 3 >= ident):
            message = choice(["Impressive\nLuck", "Wow!", "Oh\nLucky\nOne"])
        elif ( 5 >= ident ):
            message = choice(["Lucky!", "Fantastic\nPlay", "Well\n\nPlayed"])
        elif ( 7 >= ident):
            message = choice(["Well\nDone!", "Great\nPlay", "Deductive\nReasoning"])
        elif (cntlevels-1 == ident):
            message = choice(["A\nSqueaker!", "Too\nClose!", "Whew!"])
        else:
            message = "That\nwas\nClose!"
    return message


# Representation of the MasterMind game logic.
class Game:

    # Object initialization.
    def __init__( self, board ):
        self.board = board
        board.draw()


    # Generate the color list needed for the game.
    def __genColorList(self) :
        cntcolors = self.board.getColorCount()
        cntpositions = self.board.getPositionCount()
        colorids = []
        while (cntpositions):
            cntpositions -= 1
            colorids.append(randint(0, cntcolors-1))
        return colorids


    # Determines match colors (blacks and whites)
    def __matchColors(self, ident):
        blacks = whites = 0
        colorslvl = self.board.getPattern(ident)
        if None not in colorslvl:
            colorssln = self.board.getSolutionPattern()
#            print(colorssln, colorslvl)
            for i in range(len(colorssln)):
                if (colorssln[i] == colorslvl[i]):
                    blacks += 1
                    colorslvl[i] = -1
                    colorssln[i] = -2
#                    print(colorssln, colorslvl)

            for i in range(len(colorssln)):
                for k in range(len(colorslvl)):
                    if (colorssln[i] == colorslvl[k]):
                        whites += 1
                        colorslvl[k] = -1
                        colorssln[i] = -2
#                        print(colorssln, colorslvl)

        return blacks, whites


    # Determine if level has been completed.
    def __isLevelComplete(self, ident):
        return (None not in (self.board.getPattern(ident)))


    # This is the primary MasterMind logic.
    def __playLevels(self):
        self.board.setMessagePanelText("Ready\nto\nPlay")
        self.board.setActionButtonText("Show Me")

        cntlevels = self.board.getLevelCount()
        cntpositions = self.board.getPositionCount()

        ident = 0
        action = None
        fNoMoreTurns = fWonGame = False
        while (not fNoMoreTurns and not fWonGame):
            pnt = self.board.getMouse()
            action = self.board.clicked(pnt)
            if (Board.PANEL_COLORS == action):
                colorindex = self.board.clickedColor(pnt)
                if (None != colorindex):
                    self.board.setToken(ident,colorindex)
                    if (self.__isLevelComplete(ident)):
                        blacks, whites = self.__matchColors(ident)
                        self.board.setMatches(ident, blacks, whites)
                        ident += 1
                        fNoMoreTurns = (ident == cntlevels-1)
                        fWonGame = (blacks == cntpositions)

            if (Board.PANEL_GAME == action):
                level,token = self.board.clickedLevel(pnt)
                if (None != level) and (None !=token) and (level == ident):
                    self.board.clearToken(level, token)

            if (Board.BUTTON_ACTION == action):
                self.board.showSolutionPattern()
                action = None
                break

            if (Board.BUTTON_EXIT == action):
                break

        self.board.showSolutionPattern()
        self.board.setActionButtonText("Play Again")
        message = _gameExitMessage(fWonGame, ident, cntlevels)
        self.board.setMessagePanelText(message)
        return action


    # Commence playing MasterMind game.
    def play(self):
        action = None
        while (Board.BUTTON_EXIT != action):
            self.board.reset()
            self.board.setSolutionPattern(self.__genColorList())
            action = self.__playLevels()

            while (Board.BUTTON_EXIT != action) and (Board.BUTTON_ACTION != action):
                pnt = self.board.getMouse()
                action = self.board.clicked(pnt)