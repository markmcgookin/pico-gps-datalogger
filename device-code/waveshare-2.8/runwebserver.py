# Bootstrap
import board
import digitalio
from digitalio import DigitalInOut, Direction
import displayio
import supervisor
import time
from adafruit_debouncer import Debouncer

# Local
import waveshareDisplay
from waveshareDisplay import updateText

try:
    from usersecrets import usersecrets
except ImportError:
    print("WiFi secrets are kept in usersecrets.py, please add them there!")
    raise

# WebServer
import os
import ipaddress
import wifi
import socketpool
import busio
import microcontroller
import terminalio
#from adafruit_display_text import label
#import adafruit_displayio_ssd1306
#import adafruit_imageload
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType
#from adafruit_onewire.bus import OneWireBus
#from adafruit_ds18x20 import DS18X20

# ON BOARD LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

position_A_input = digitalio.DigitalInOut(board.GP2)
position_A_input.switch_to_input(pull=digitalio.Pull.UP)
position_A = Debouncer(position_A_input);

position_B_input = digitalio.DigitalInOut(board.GP3)
position_B_input.switch_to_input(pull=digitalio.Pull.UP)
position_B = Debouncer(position_B_input);

wifi.radio.connect(usersecrets["ssid"], usersecrets["password"])
updateText("Connected to %s!" % usersecrets["ssid"])
time.sleep(1)
updateText("my IP addr: %s" % wifi.radio.ipv4_address)
time.sleep(2)

pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)

#  variables for HTML
#  comment/uncomment desired temp unit

#  temp_test = str(ds18.temperature)
#  unit = "C"
#temp_test = str(c_to_f(ds18.temperature))
#unit = "F"
#  font for HTML
font_family = "monospace"

#  the HTML script
#  setup as an f string
#  this way, can insert string variables from code.py directly
#  of note, use {{ and }} if something from html *actually* needs to be in brackets
#  i.e. CSS style formatting
def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    html{{font-family: {font_family}; background-color: lightgrey;
    display:inline-block; margin: 0px auto; text-align: center;}}
      h1{{color: deeppink; width: 200; word-wrap: break-word; padding: 2vh; font-size: 35px;}}
      p{{font-size: 1.5rem; width: 200; word-wrap: break-word;}}
      .button{{font-family: {font_family};display: inline-block;
      background-color: black; border: none;
      border-radius: 4px; color: white; padding: 16px 40px;
      text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}}
      p.dotted {{margin: auto;
      width: 75%; font-size: 25px; text-align: center;}}
    </style>
    </head>
    <body>
    <title>Pico W HTTP Server</title>
    <h1>Hello World!!!</h1>
    <form accept-charset="utf-8" method="POST">
    <button class="button" name="LED ON" value="ON" type="submit">LED ON</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="LED OFF" value="OFF" type="submit">LED OFF</button></a></p></form>
    </body></html>
    """
    return html

#  route default static IP
@server.route("/")
def base(request: HTTPRequest):  # pylint: disable=unused-argument
    #  serve the HTML f string
    #  with content type text/html
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

#  if a button is pressed on the site
@server.route("/", method=HTTPMethod.POST)
def buttonpress(request):
    #  get the raw text
    raw_text = request.raw_request.decode("utf8")
    print(raw_text)
    #  if the led on button was pressed
    if "ON" in raw_text:
        #  turn on the onboard LED
        led.value = True
    #  if the led off button was pressed
    if "OFF" in raw_text:
        #  turn the onboard LED off
        led.value = False
    #  reload site
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

print("starting server..")
# startup the server
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
#  if the server fails to begin, restart the pico w
except OSError:
    time.sleep(5)
    print("restarting..")
    microcontroller.reset()
ping_address = ipaddress.ip_address("8.8.4.4")


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
        waveshareDisplay.enableDisableDisplay(False)

    #Poll the webserver for new requests
    server.poll()
