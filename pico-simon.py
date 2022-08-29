'''
About  : Top-level module for Pico Simon game.
Version: 1 (29-Aug-2022)
Author : Kevin Morley
'''

# ------------------------------------------------------------------------------

import logging

from hardware import LOG_LEVEL
from game import Game

# ------------------------------------------------------------------------------
# Set module-level logging.
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

# ------------------------------------------------------------------------------

try:
    # create game object
    game = Game()
    # wait for reset button to be pressed
    game.wait_start()

except Exception as ex:
    log.exc(ex, 'Exception occurred:')

# ------------------------------------------------------------------------------

'''
End
'''
