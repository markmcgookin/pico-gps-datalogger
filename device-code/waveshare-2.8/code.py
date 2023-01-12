import board
import digitalio
import busio
import time
from adafruit_debouncer import Debouncer

# New stuff for GPS module
import adafruit_gps

# Display stuff
import waveshareDisplay

# ON BOARD LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

position_A_input = digitalio.DigitalInOut(board.GP2)
position_A_input.switch_to_input(pull=digitalio.Pull.UP)
position_A = Debouncer(position_A_input);

position_B_input = digitalio.DigitalInOut(board.GP3)
position_B_input.switch_to_input(pull=digitalio.Pull.UP)
position_B = Debouncer(position_B_input);

# UART GPS Stuff
# Setup/Define a bunch of stuff.
TX = board.GP0
RX = board.GP1

uart = busio.UART(TX, RX, baudrate=9600, timeout=30)
gps = adafruit_gps.GPS(uart, debug=False)

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b'PMTK220,1000')
last_print = time.monotonic()

# Clock, MOSI, MISO
spi = busio.SPI(board.GP10, board.GP11, board.GP12)
waveshareDisplay.setupDisplay(spi)

while True:
    current = time.monotonic()

    position_A.update()
    position_B.update()

    if position_A.fell:
        print("In position A")
    elif position_A.rose:
        print("Left position A")

    if position_B.fell:
        print("In position B")
    elif position_B.rose:
        print("Left position B")

    if current - last_print >= 1.0:
        last_print = current

        print("Update GPS")
        gps.update()

        print("Blink")
        if led.value == True:
            led.value = False
        else:
            led.value = True

        if not gps.has_fix:
            # TODO - Flash NeoPixel Red.
            print('Waiting for fix...')
            continue

        position = "Latitude: {0:.6f} degrees. Longitude: {1:.6f} degrees".format(gps.latitude, gps.longitude)
        print(position)
