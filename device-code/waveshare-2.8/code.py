import board
import digitalio
import displayio
import time
from adafruit_debouncer import Debouncer

# Local
import waveshareDisplay
from waveshareDisplay import updateText

# ON BOARD LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

position_A_input = digitalio.DigitalInOut(board.GP2)
position_A_input.switch_to_input(pull=digitalio.Pull.UP)
position_A = Debouncer(position_A_input);

position_B_input = digitalio.DigitalInOut(board.GP3)
position_B_input.switch_to_input(pull=digitalio.Pull.UP)
position_B = Debouncer(position_B_input);

button_blue_input = digitalio.DigitalInOut(board.GP17)
button_blue_input.switch_to_input(pull=digitalio.Pull.UP)
button_blue = Debouncer(button_blue_input);

button_red_input = digitalio.DigitalInOut(board.GP16)
button_red_input.switch_to_input(pull=digitalio.Pull.UP)
button_red = Debouncer(button_red_input);

def modeSelect():
    position_A.update()
    position_B.update()

    if position_A.value and position_B.value:
        updateText("Switch in the middle")
        waveshareDisplay.enableDisableDisplay(False)
    else:
        # We are going to run a functional mode - Release the pins and/or kracken
        led.deinit()
        position_A_input.deinit()
        position_B_input.deinit()

        # Enable the screen
        waveshareDisplay.enableDisableDisplay(True)

        if position_A.value:
            updateText("Switch down below")
            #Run the webserver
            import runwebserver
        elif position_B.value:
            updateText("Switch up top")
            #Run the GPS Code
            import rungps


modeSelect()

# So the switch was in the middle, monitor for changes
#if position_A.value and position_B.value:
#    while True:
#        modeSelect()


import board
import digitalio
import displayio
import time
from adafruit_debouncer import Debouncer

# Local
import waveshareDisplay
from waveshareDisplay import updateText

# ON BOARD LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

position_A_input = digitalio.DigitalInOut(board.GP2)
position_A_input.switch_to_input(pull=digitalio.Pull.UP)
position_A = Debouncer(position_A_input);

position_B_input = digitalio.DigitalInOut(board.GP3)
position_B_input.switch_to_input(pull=digitalio.Pull.UP)
position_B = Debouncer(position_B_input);

button_blue_input = digitalio.DigitalInOut(board.GP17)
button_blue_input.switch_to_input(pull=digitalio.Pull.UP)
button_blue = Debouncer(button_blue_input);

button_red_input = digitalio.DigitalInOut(board.GP16)
button_red_input.switch_to_input(pull=digitalio.Pull.UP)
button_red = Debouncer(button_red_input);

def modeSelect():
    position_A.update()
    position_B.update()

    if position_A.value and position_B.value:
        updateText("Switch in the middle")
        waveshareDisplay.enableDisableDisplay(False)
    else:
        # We are going to run a functional mode - Release the pins and/or kracken
        led.deinit()
        position_A_input.deinit()
        position_B_input.deinit()

        # Enable the screen
        waveshareDisplay.enableDisableDisplay(True)

        if position_A.value:
            updateText("Switch down below")
            #Run the webserver
            import runwebserver
        elif position_B.value:
            updateText("Switch up top")
            #Run the GPS Code
            import rungps


modeSelect()

# So the switch was in the middle, monitor for changes
if position_A.value and position_B.value:
   while True:
       modeSelect()


# while True:
#     button_blue.update()
#     button_red.update()
    
#     if button_blue.fell:
#         print('Blue Just pressed')
#     if button_blue.rose:
#         print('Blue Just released')

#     if button_red.fell:
#         print('Red Just pressed')
#     if button_red.rose:
#         print('Red Just released')
