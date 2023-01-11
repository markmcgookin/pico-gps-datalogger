import board
import busio
import terminalio
import displayio
import neopixel
import time
import digitalio

import os
import sdcardio
import storage
import sys

from adafruit_display_text import label
from adafruit_st7789 import ST7789

import directory_functions

# ON BOARD LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Release any resources currently in use for the displays
displayio.release_displays()

tft_dc = board.GP8
tft_cs = board.GP9
tft_rst = board.GP15

tft_bl = digitalio.DigitalInOut(board.GP13)
tft_bl.direction = digitalio.Direction.OUTPUT
tft_bl.value = True

# Clock, MOSI, MISO
spi = busio.SPI(board.GP10, board.GP11, board.GP12)

# Mount and test the SD Card
directory_functions.mount_sd_card(spi)
directory_functions.print_directory("/sd")

print(str(spi.frequency))

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, width=320, height=240, rotation=90)

print(str(spi.frequency))

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(280, 200, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group(scale=3, x=57, y=120)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

count = 0
last_print = time.monotonic()
while True:
    current = time.monotonic()

    if current - last_print >= 1.0:
        last_print = current

        #print("Loop " + str(count))
        count = count + 1

        if led.value == True:
            led.value = False
        else:
            led.value = True
