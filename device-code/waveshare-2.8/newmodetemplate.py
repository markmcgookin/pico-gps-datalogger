# Bootstrap
import board
import digitalio
import displayio
import supervisor
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

# Clock, MOSI, MISO
while True:

    current = time.monotonic()

    position_A.update()
    position_B.update()

    if position_B.fell:
        # Switch moved to the up position from the middle, turn on the display
        print("B fell, enabling display")
        waveshareDisplay.enableDisableDisplay(True)
    elif position_B.rose:
        # Switch moved down from the up position to the middle, just turn off the screen
        print("B rose, disabling display")
        waveshareDisplay.enableDisableDisplay(False)
    if position_A.fell:
        #waveshareDisplay.enableDisableDisplay(True)
        #switch moved into the bottom position... reset the pico
        # this will force it to reload, detect the switch is down,
        # and boot in the appropriate mode
        print("A fell, rebooting")
        supervisor.reload()
    elif position_B.rose:
        waveshareDisplay.enableDisableDisplay(False)# Write your code here :-)
