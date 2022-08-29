'''
About  : Top-level module for Pico Simon game.
Version: 1 (29-Aug-2022)
Author : Kevin Morley
'''

# ------------------------------------------------------------------------------

from game import Game

# ------------------------------------------------------------------------------

# create game object
game = Game()
# wait for reset button to be pressed before beginning game
game.wait_start()

# ------------------------------------------------------------------------------

'''
End
'''
