#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: MasterMind primary program.
#
#  $RCSfile: MasterMind.py $
#
#   Started:
# $Revision: 1.3 $
#     $Date: 2009/12/01 18:02:23 $
##


from __future__ import print_function
from board import Board
from game import Game


if __name__=='__main__':
    
    sizey = 800
    board = Board(sizey)
    game  = Game(board)
    game.play()
    
    # Forced cleanup of board object.
    board.close()