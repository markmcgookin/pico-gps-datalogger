# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text..
"""
import board
import busio
import terminalio
import displayio
import neopixel
import time
import digitalio

from adafruit_display_text import label
from adafruit_st7789 import ST7789

# New stuff for GPS module
import adafruit_gps

# New stuff for SD card
import directory_functions

print("Starting")

sdCardPresent = False
try:
    # Mount the SD card and print its contents
    directory_functions.mount_sd_card()
    directory_functions.print_directory("/sd")
    sdCardPresent = True
except:
    print("No SD Card")
    
# UART GPS Stuff
# Setup/Define a bunch of stuff.
RX = board.GP1
TX = board.GP0
uart = busio.UART(TX, RX, baudrate=9600, timeout=30)
gps = adafruit_gps.GPS(uart, debug=False)

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b'PMTK220,1000')

# ON BOARD LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


# NEOPIXEL
pixels = neopixel.NeoPixel(board.GP28, 1, auto_write=False, brightness=0.1)

def setNeoPixel(r, g, b):
    pixels[0] = (r, g, b)
    pixels.show()

setNeoPixel(255,0,255)
neoPixelOn = True

# Setup stuff for display
BORDER_WIDTH = 28
TEXT_SCALE = 2

# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GP5
tft_dc = board.GP6
tft_rst = board.GP7

spi = busio.SPI(board.GP2, board.GP3, board.GP4)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)

display = ST7789(display_bus, width=320, height=172, colstart=34, rotation=270)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(
    display.width - (BORDER_WIDTH * 2), display.height - (BORDER_WIDTH * 2), 1
)

inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER_WIDTH, y=BORDER_WIDTH
)
splash.append(inner_sprite)

screen_text = ""
if sdCardPresent:
    screen_text = "SD Card Found"
else: 
    screen_text = "No SD Card"

def updateTextArea(displayText):
    return label.Label(
    terminalio.FONT,
    text=displayText,
    color=0xFFFF00,
    scale=TEXT_SCALE,
    anchor_point=(0.5, 0.5),
    anchored_position=(display.width // 2, display.height // 2),
)

# Draw a label.
text_area = updateTextArea(screen_text)
splash.append(text_area)

last_print = time.monotonic()
filename = directory_functions.get_next_logfilename("/sd", "gps_logfile")
    
print("Got filename: " + filename)
lasterror = ""
lastTime = ""
count = 0

while True:
    try:
        current = time.monotonic()
        
        if lasterror != "":
            print("Last error: " + lasterror)
            with open(filename, "w") as f:
                f.write("Caught Value Error, last time seen: " + lastTime)
                f.flush()

        if current - last_print >= 1.0:
            last_print = current
            
            print("Loop " + str(count))
            count = count + 1
            
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
                splash.remove(text_area)
                text_area = updateTextArea("Waiting for fix...")
                splash.append(text_area)

                if neoPixelOn:
                    setNeoPixel(0,0,0) #Flash it off
                    neoPixelOn = False
                else:
                    setNeoPixel(255,0,0) #Flash it red
                    neoPixelOn = True
                continue

            # We have a GPS fix
            if neoPixelOn:
                setNeoPixel(0,0,0) #Flash it off
                neoPixelOn = False
            else:
                setNeoPixel(0,0,255) #Flash it red
                neoPixelOn = True
            
            position = "Latitude: {0:.6f} degrees. Longitude: {1:.6f} degrees".format(gps.latitude, gps.longitude)
            text_area = updateTextArea("Waiting for fix...")
                
            if sdCardPresent:
                with open(filename, "w") as f:
                    print('=' * 40)
                    f.write('=' * 40)
                    lastTime = "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                            gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                            gps.timestamp_utc.tm_mday,  # struct_time object that holds
                            gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                            gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                            gps.timestamp_utc.tm_min,  # month!
                            gps.timestamp_utc.tm_sec,
                        )

                    print(lastTime)
                    f.write(lastTime)

                    print("Latitude: {0:.6f} degrees".format(gps.latitude))
                    f.write("Latitude: {0:.6f} degrees".format(gps.latitude))

                    print("Longitude: {0:.6f} degrees".format(gps.longitude))
                    f.write("Longitude: {0:.6f} degrees".format(gps.longitude))

                    print(
                        "Precise Latitude: {:2.}{:2.4f} degrees".format(
                            gps.latitude_degrees, gps.latitude_minutes
                        )
                    )
                    f.write
                    (
                        "Precise Latitude: {:2.}{:2.4f} degrees".format(
                            gps.latitude_degrees, gps.latitude_minutes
                        )
                    )

                    print(
                        "Precise Longitude: {:2.}{:2.4f} degrees".format(
                            gps.longitude_degrees, gps.longitude_minutes
                        )
                    )
                    f.write(
                        "Precise Longitude: {:2.}{:2.4f} degrees".format(
                            gps.longitude_degrees, gps.longitude_minutes
                        )
                    )

                    print("Fix quality: {}".format(gps.fix_quality))
                    f.write("Fix quality: {}".format(gps.fix_quality))

                    # Some attributes beyond latitude, longitude and timestamp are optional
                    # and might not be present.  Check if they're None before trying to use!
                    if gps.satellites is not None:
                        print("# satellites: {}".format(gps.satellites))
                        f.write("# satellites: {}".format(gps.satellites))
                    if gps.altitude_m is not None:
                        print("Altitude: {} meters".format(gps.altitude_m))
                        f.write("Altitude: {} meters".format(gps.altitude_m))
                    if gps.speed_knots is not None:
                        print("Speed: {} knots".format(gps.speed_knots))
                        f.write("Speed: {} knots".format(gps.speed_knots))
                    if gps.track_angle_deg is not None:
                        print("Track angle: {} degrees".format(gps.track_angle_deg))
                        f.write("Track angle: {} degrees".format(gps.track_angle_deg))
                    if gps.horizontal_dilution is not None:
                        print("Horizontal dilution: {}".format(gps.horizontal_dilution))
                        f.write("Horizontal dilution: {}".format(gps.horizontal_dilution))
                    if gps.height_geoid is not None:
                        print("Height geoid: {} meters".format(gps.height_geoid))
                        f.write("Height geoid: {} meters".format(gps.height_geoid))

                    f.flush()
            else:
                print('=' * 40)
                lastTime = "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                        gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                        gps.timestamp_utc.tm_mday,  # struct_time object that holds
                        gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                        gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                        gps.timestamp_utc.tm_min,  # month!
                        gps.timestamp_utc.tm_sec,
                    )

                print(lastTime)
                print("Latitude: {0:.6f} degrees".format(gps.latitude))
                print("Longitude: {0:.6f} degrees".format(gps.longitude))

                print(
                    "Precise Latitude: {:2.}{:2.4f} degrees".format(
                        gps.latitude_degrees, gps.latitude_minutes
                    )
                )
                
                print(
                    "Precise Longitude: {:2.}{:2.4f} degrees".format(
                        gps.longitude_degrees, gps.longitude_minutes
                    )
                )
                
                print("Fix quality: {}".format(gps.fix_quality))

                # Some attributes beyond latitude, longitude and timestamp are optional
                # and might not be present.  Check if they're None before trying to use!
                if gps.satellites is not None:
                    print("# satellites: {}".format(gps.satellites))
                if gps.altitude_m is not None:
                    print("Altitude: {} meters".format(gps.altitude_m))
                if gps.speed_knots is not None:
                    print("Speed: {} knots".format(gps.speed_knots))
                if gps.track_angle_deg is not None:
                    print("Track angle: {} degrees".format(gps.track_angle_deg))
                if gps.horizontal_dilution is not None:
                    print("Horizontal dilution: {}".format(gps.horizontal_dilution))
                if gps.height_geoid is not None:
                    print("Height geoid: {} meters".format(gps.height_geoid))
    except ValueError:
        lasterror = "value error caught"

