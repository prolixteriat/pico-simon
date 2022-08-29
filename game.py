'''
About  : Game logic module for Pico Simon game.
Version: 1 (29-Aug-2022)
Author : Kevin Morley
'''

# ------------------------------------------------------------------------------

import hardware
import math
import random
import utime

# ------------------------------------------------------------------------------

random.seed()

# ------------------------------------------------------------------------------
# Class which provides the game logic.

class Game:
    
    # --------------------------------------------------------------------------
    # Constructor
    
    def __init__(self):
        
        self.notes = []    # current sequence of notes
        self.duration = 0  # duration (ms) of LED & tone activations
        self.hw = hardware.Hardware() # object which manages hardware interactions
        self.play_start()  # play game start fanfare

    # --------------------------------------------------------------------------
    # Add a random new colour to the existing sequence.
    
    def add_colour(self):
        
        colour = random.choice(hardware.COLOURS)
        self.notes.append(colour)
        count = len(self.notes)
        # increase speed every 4 notes
        if (count % 4 == 0):
            self.duration = math.floor(self.duration * 0.75) 
        
        self.play_all_colours(self.duration)

    # --------------------------------------------------------------------------
    # Play a new game .
    
    def play(self):
        
        # initialise game
        self.notes.clear()
        self.duration = 500
        # keep adding adding & reading colours until user error occurs
        self.add_colour()
        while (self.read_colours() is True):
            utime.sleep(1)
            self.add_colour()
        
        # user error has occurred
        self.play_fail()
        self.play_all_colours(200)
        self.wait_start()
            
    # --------------------------------------------------------------------------
    # Play the current sequence of colours with the provided note duration (ms).
    
    def play_all_colours(self, duration):
        
        for n in self.notes:
            self.hw.play_colour(n, duration)
            
    # --------------------------------------------------------------------------
    # Play the failure notification fanfare.
    
    def play_fail(self):
        
        utime.sleep(1)
        for c in hardware.COLOURS:
            self.hw.light_led(c, True)
            
        self.hw.play_tone(hardware.NOTE_G2, 250)
        self.hw.play_tone(hardware.NOTE_C2, 500)

        utime.sleep(1)
        for c in hardware.COLOURS:
            self.hw.light_led(c, False)

    # --------------------------------------------------------------------------
    # Play the power-on fanfare.
    
    def play_start(self):
        
        for c in hardware.COLOURS:
            self.hw.play_colour(c, 100)
            
        for c in reversed(hardware.COLOURS):
            self.hw.play_colour(c, 100)
    
    # --------------------------------------------------------------------------
    # Read button presses comparing against the current sequence as we go.
    # Return True if button presses match sequence, else return False.
    
    def read_colours(self):
        
        ok = True
        for n in self.notes:
            colour = self.hw.get_button_press()
            # check whether reset button has been pressed
            if (colour is None):
                self.play_fail()
                self.play()
                
            self.hw.play_colour(colour, 250)
            if (colour != n):
                ok = False
                break
            
        return ok
           
    # --------------------------------------------------------------------------
    # Wait for a reset button press and then call method to play the game. 
    
    def wait_start(self):
        
        if (self.hw.get_reset_press() is True):
            self.play()
                    
    # --------------------------------------------------------------------------

'''
End
'''

