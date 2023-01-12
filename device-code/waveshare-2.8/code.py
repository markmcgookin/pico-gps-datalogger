import board
import digitalio
import busio
import time
import displayio
import adafruit_gps

# Wifi
import time
import ssl
import socketpool
import wifi
import adafruit_requests

# Local
import waveshareDisplay
from waveshareDisplay import updateText
from directory_functions import print_directory, get_next_logfilename, log_gps_data

print_directory("/sd")

# Switch/Button
from adafruit_debouncer import Debouncer

try:
    from usersecrets import usersecrets
except ImportError:
    print("WiFi secrets are kept in usersecrets.py, please add them there!")
    raise

# ON BOARD LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

position_A_input = digitalio.DigitalInOut(board.GP2)
position_A_input.switch_to_input(pull=digitalio.Pull.UP)
position_A = Debouncer(position_A_input);

position_B_input = digitalio.DigitalInOut(board.GP3)
position_B_input.switch_to_input(pull=digitalio.Pull.UP)
position_B = Debouncer(position_B_input);

position_A.update()
position_B.update()

if position_A.value and position_B.value:
    waveshareDisplay.enableDisableDisplay(False)
else:
    waveshareDisplay.enableDisableDisplay(True)

waiting_cursor_position = 0
waiting_cursor = ["", ".", "..", "..."]

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

# Wifi Stuff
updateText("Connecting to %s" % usersecrets["ssid"])
time.sleep(1)
wifi.radio.connect(usersecrets["ssid"], usersecrets["password"])
updateText("Connected to %s!" % usersecrets["ssid"])
time.sleep(1)
updateText("my IP addr: %s" % wifi.radio.ipv4_address)
time.sleep(2)

pool = socketpool.SocketPool(wifi.radio)
request = adafruit_requests.Session(pool, ssl.create_default_context())

updateText("Fetching wifitest.adafruit.com...");
time.sleep(1)
response = request.get("http://wifitest.adafruit.com/testwifi/index.html")
updateText(str(response.status_code))
time.sleep(2)
updateText(response.text)


last_print = time.monotonic()
filename = get_next_logfilename("/sd", "gps_logfile")
print("Got filename: " + filename)

# Clock, MOSI, MISO
while True:
    current = time.monotonic()

    position_A.update()
    position_B.update()

    if position_A.fell:
        waveshareDisplay.enableDisableDisplay(True)
    elif position_A.rose:
        waveshareDisplay.enableDisableDisplay(False)

    if position_B.fell:
        waveshareDisplay.enableDisableDisplay(True)
    elif position_B.rose:
        waveshareDisplay.enableDisableDisplay(False)

    if current - last_print >= 1.0:
        last_print = current
        gps.update()
        if led.value == True:
            led.value = False
        else:
            led.value = True

        if not gps.has_fix:
            # TODO - Flash NeoPixel Red.
            cursor = waiting_cursor[waiting_cursor_position]

            updateText("Waiting for GPS Fix" + cursor)
            if waiting_cursor_position == 3:
                waiting_cursor_position = 0
            else:
                waiting_cursor_position = waiting_cursor_position + 1
            continue

        position = "Latitude: {0:.6f} degrees. /n Longitude: {1:.6f} degrees".format(gps.latitude, gps.longitude)
        updateText(position)
        log_gps_data(gps, filename)
