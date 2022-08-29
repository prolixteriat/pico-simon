'''
About  : Hardware interface module for Pico Simon game.
Version: 1 (29-Aug-2022)
Author : Kevin Morley
'''

# ------------------------------------------------------------------------------

import machine
import utime

# ------------------------------------------------------------------------------
# Define musical frequencies (Hz).
# See https://pages.mtu.edu/~suits/notefreqs.html
NOTE_G2 = 98 
NOTE_C2 = 65 
NOTE_E3 = 165 
NOTE_C4S = 277 
NOTE_E4 = 330 
NOTE_A4 = 440 

# Assign notes to constants representing colours.
NOTE_YELLOW = NOTE_C4S
NOTE_BLUE = NOTE_E4
NOTE_RED = NOTE_A4
NOTE_GREEN = NOTE_E3

# GPIO pin numbers for LEDs, buttons and passive buzzer.
PIN_LED_YELLOW = 17
PIN_LED_BLUE = 18
PIN_LED_RED = 19
PIN_LED_GREEN = 20
PIN_BUT_YELLOW = 15
PIN_BUT_BLUE = 14
PIN_BUT_RED = 13
PIN_BUT_GREEN = 12
PIN_BUT_RESET = 11
PIN_SPEAKER = 16

# Text representations of colours.
BLUE = 'blue'
GREEN = 'green'
RED = 'red'
YELLOW = 'yellow'

# Array of all colours. Order to match physical layout of LEDs for lightshow.
COLOURS = [GREEN, RED, BLUE, YELLOW]
    
# --------------------------------------------------------------------------
# Class which provides all hardware IO.

class Hardware:
    
    # --------------------------------------------------------------------------
    # Constructor .
    
    def __init__(self):
        '''
        self.out is a dictionary with a key for each colour and a corresponding
        value which is a dictionary of a button object, LED object and a tone
        frequency associated with that particular colour.
        '''
        self.out = {}
        self.out[BLUE] = self.config_colour(PIN_BUT_BLUE, PIN_LED_BLUE, NOTE_BLUE)
        self.out[GREEN] = self.config_colour(PIN_BUT_GREEN, PIN_LED_GREEN, NOTE_GREEN)
        self.out[RED] = self.config_colour(PIN_BUT_RED, PIN_LED_RED, NOTE_RED)
        self.out[YELLOW] = self.config_colour(PIN_BUT_YELLOW, PIN_LED_YELLOW, NOTE_YELLOW)
        # passive buzzer
        self.speaker = machine.PWM(machine.Pin(PIN_SPEAKER))
        # reset button
        self.reset = machine.Pin(PIN_BUT_RESET, machine.Pin.IN, machine.Pin.PULL_UP)
        
    # --------------------------------------------------------------------------
    # Configure hardware setttings associated with a single colour. Return dictionary.
    
    def config_colour(self, pin_button, pin_led, note):
        
        config = {
            'button': machine.Pin(pin_button, machine.Pin.IN, machine.Pin.PULL_UP),
            'led': machine.Pin(pin_led, machine.Pin.OUT),
            'note': note
            }
        return config
    
    # --------------------------------------------------------------------------
    # Wait for a button to be pressed. Return colour of button, or None if reset pressed.
    
    def get_button_press(self):
        
        while True:
            for c in COLOURS:
                v = self.out[c]['button'].value()
                if (v == 0):
                    return c
                
            v = self.reset.value()
            if (v == 0):
                return None
            
            utime.sleep_ms(100)
         
    # --------------------------------------------------------------------------
    # Wait for the reset button to be pressed. Return True when pressed.
    
    def get_reset_press(self):
        
        print('Hardware:get_reset_press(): Waiting for reset button to be pressed...')
        while True:
            v = self.reset.value()
            if (v == 0):
                return True
            
            utime.sleep_ms(100)
            
    # --------------------------------------------------------------------------
    # Turn a specific colour LED on or off.
    
    def light_led(self, colour, state):

        cfg = self.out[colour]
        cfg['led'].value(state)
        
    # --------------------------------------------------------------------------
    # play the tone and light the LED for a given colour for a given duration (ms)
    
    def play_colour(self, colour, duration):
        
        self.light_led(colour, True)
        cfg = self.out[colour]
        self.play_tone(cfg['note'], duration)
        self.light_led(colour, False)
        
    # --------------------------------------------------------------------------
    # play a given tone (Hz) for a given duration (ms)
    
    def play_tone(self, tone, duration):
        
        self.speaker.freq(tone)
        self.speaker.duty_u16(30000)
        utime.sleep_ms(duration)
        self.speaker.duty_u16(0)
        utime.sleep_ms(duration)
       
    # --------------------------------------------------------------------------

'''
End
'''
        