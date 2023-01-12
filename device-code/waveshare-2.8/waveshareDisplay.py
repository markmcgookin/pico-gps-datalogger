import time
import board
import busio
import displayio
import digitalio
import fontio
import sdcardio
import storage
import sys
import terminalio

from text_functions import wrap_nicely

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label, bitmap_label
from adafruit_st7789 import ST7789

tft_dc = board.GP8
tft_cs = board.GP9
tft_rst = board.GP15
tft_bl = digitalio.DigitalInOut(board.GP13)
tft_bl.direction = digitalio.Direction.OUTPUT
tft_bl.value = True

displayio.release_displays()
spi = busio.SPI(board.GP10, board.GP11, board.GP12)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, width=320, height=240, rotation=90)

main_group = displayio.Group()
MEDIUM_FONT = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")
TIME_PAUSE = 2

#bitmap = displayio.Bitmap(4, display.width, 2)
palette = displayio.Palette(2)
palette[0] = 0x004400
palette[1] = 0x00FFFF
#horizontal_line = displayio.TileGrid(bitmap, pixel_shader=palette, x=155, y=0)
#main_group.append(horizontal_line)

#bitmap = displayio.Bitmap(display.width, 4, 2)
#vertical_line = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=110)
#main_group.append(vertical_line)

# Tests
header_text_area = label.Label(MEDIUM_FONT, text="GPS POSITION")
header_text_area.x = 10
header_text_area.y = 11
main_group.append(header_text_area)
display.show(main_group)

body_text_area = label.Label(terminalio.FONT, text="")
body_text_area.x = 10
body_text_area.y = 30
main_group.append(body_text_area)
display.show(main_group)

# Testing Text Setter
body_text_area.text = wrap_nicely("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore", 45)
display.show(main_group)
time.sleep(TIME_PAUSE)

# Testing Text Setter
body_text_area.text = wrap_nicely("Do, or do not, there is no try", 45)
display.show(main_group)
time.sleep(TIME_PAUSE)

sd_card_cs = board.GP22
sdcard = sdcardio.SDCard(spi, sd_card_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
sys.path.append("/sd")

def file_exists(filename):
    file_exists = False
    try:
        os.stat(filename)
        file_exists = True
    except OSError:
        file_exists = False
    return file_exists

def updateText(bodyText):
    print(bodyText)
    body_text_area.text = wrap_nicely(bodyText, 45)

def enableDisableDisplay(backlightValue):
    tft_bl.value = backlightValue

def adafruit_example():
    # SPDX-FileCopyrightText: 2021 Jose David M.
    #
    # SPDX-License-Identifier: MIT
    #############################
    """
    This is an advanced demonstration of the display_text library capabilities
    """

    displayio.release_displays()
    spi = busio.SPI(board.GP10, board.GP11, board.GP12)
    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
    display = ST7789(display_bus, width=320, height=240, rotation=90)

    main_group = displayio.Group()
    MEDIUM_FONT = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")
    BIG_FONT = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")
    TIME_PAUSE = 2

    bitmap = displayio.Bitmap(4, display.width, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x004400
    palette[1] = 0x00FFFF
    horizontal_line = displayio.TileGrid(bitmap, pixel_shader=palette, x=155, y=0)
    main_group.append(horizontal_line)

    bitmap = displayio.Bitmap(display.width, 4, 2)
    vertical_line = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=110)
    main_group.append(vertical_line)

    # Tests
    header_text_area = label.Label(terminalio.FONT, text="Circuit Python")
    main_group.append(header_text_area)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Testing position setter
    header_text_area.x = 10
    header_text_area.y = 10
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Testing creating label with initial position
    header_text_area.text = "Testing initiating without text"
    try:
        body_text_area = label.Label(terminalio.FONT)
    except SyntaxError:
        print("Fail setting-up label without text")
        warning_text = label.Label(
            BIG_FONT,
            text="Test Fail",
            x=display.width // 2,
            y=display.height // 4,
            background_color=0x004499,
        )
        main_group.append(warning_text)

    display.show(main_group)
    time.sleep(TIME_PAUSE)

    header_text_area.text = "Testing Position"
    body_text_area = label.Label(
        terminalio.FONT, text="Circuit", x=display.width // 2, y=display.height // 2
    )
    main_group.append(body_text_area)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Testing Text Setter
    header_text_area.text = "Testing Changing Text"
    body_text_area.text = "Python"
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Testing a and y getter and setter
    header_text_area.text = "Testing Changing Position"
    body_text_area.x = body_text_area.x - 50
    body_text_area.y = body_text_area.y - 50
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Testing font Getter and setter
    header_text_area.text = "Testing Changing FONT"
    if isinstance(body_text_area.font, fontio.BuiltinFont):
        body_text_area.font = MEDIUM_FONT
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Once this working we create another label with all the initial specs
    main_group.pop()

    # Testing Color
    header_text_area.text = "Testing Color"
    text_initial_specs = label.Label(
        MEDIUM_FONT,
        text="Circuit Python",
        x=display.width // 2,
        y=display.height // 2,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    text_initial_specs.color = 0x004400
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    # Testing Background Color
    header_text_area.text = "Testing Background Color"
    text_initial_specs = label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    text_initial_specs.background_color = 0x990099
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    # Testing Background Color
    header_text_area.text = "Testing Background Tight"
    text_initial_specs = label.Label(
        BIG_FONT,
        text="aaaaq~",
        x=0,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        background_tight=True,
    )
    main_group.append(text_initial_specs)
    text_initial_specs = label.Label(
        BIG_FONT,
        text="aaaaq~",
        x=90,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        background_tight=False,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()
    main_group.pop()

    # Testing Padding
    header_text_area.text = "Testing Padding"
    text_initial_specs = label.Label(
        BIG_FONT,
        text="CircuitPython",
        x=display.width // 4,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    # Testing Anchor Point/ Anchored Position
    header_text_area.text = "Testing Anchor Point/Anchored Position"
    text_initial_specs = label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    try:
        text_initial_specs.anchored_position = (100, 100)
        text_initial_specs.anchor_point = (0.5, 0.5)

    except TypeError:
        print("Test is failing here")
        main_group.pop()
        warning_text = label.Label(
            BIG_FONT,
            text="Test Fail",
            x=display.width // 2,
            y=display.height // 4,
            background_color=0x004499,
        )
        main_group.append(warning_text)
        time.sleep(TIME_PAUSE)
        display.show(main_group)

    main_group.pop()

    # Testing Scale
    header_text_area.text = "Testing Scale"
    text_initial_specs = label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    text_initial_specs.scale = 2
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    # Testing Base Alignment
    header_text_area.text = "Testing Base Alignment"
    text_initial_specs = label.Label(
        MEDIUM_FONT,
        text="python",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        base_alignment=True,
    )
    main_group.append(text_initial_specs)
    text_initial_specs = label.Label(
        BIG_FONT,
        text="circuit",
        x=display.width // 2 - 100,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        base_alignment=True,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()
    main_group.pop()

    # Testing Direction
    header_text_area.text = "Testing Direction-UPR"
    text_initial_specs = label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
        label_direction="UPR",
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    header_text_area.text = "Testing Direction-DWR"
    text_initial_specs = label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
        label_direction="DWR",
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    header_text_area.text = "Testing Direction-TTB"
    text_initial_specs = label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
        label_direction="TTB",
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    header_text_area.text = "Testing Direction-RTL"
    text_initial_specs = label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
        label_direction="RTL",
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    main_group.pop()

    # Testing creating label with initial position
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    header_text_area = bitmap_label.Label(terminalio.FONT, text="Circuit Python")
    main_group.append(header_text_area)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    # Testing position setter
    header_text_area.x = 10
    header_text_area.y = 10
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    header_text_area.text = "Testing initiating without text"
    try:
        body_text_area = label.Label(terminalio.FONT)
    except TypeError:
        print("Fail setting-up label without text")
        warning_text = label.Label(
            BIG_FONT,
            text="Test Fail",
            x=display.width // 2,
            y=display.height // 4,
            background_color=0x004499,
        )
        main_group.append(warning_text)

    # Testing creating label with initial position
    header_text_area.text = "Testing Position"
    body_text_area = bitmap_label.Label(
        terminalio.FONT, text="Circuit", x=display.width // 2, y=display.height // 2
    )
    main_group.append(body_text_area)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Testing Text Setter
    header_text_area.text = "Testing Changing Text"
    body_text_area.text = "Python"
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Testing a and y getter and setter
    header_text_area.text = "Testing Changing Position"
    body_text_area.x = body_text_area.x - 50
    body_text_area.y = body_text_area.y - 50
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Testing font Getter and setter
    header_text_area.text = "Testing Changing FONT"
    if isinstance(body_text_area.font, fontio.BuiltinFont):
        print("Font was BuiltinFont")
        body_text_area.font = MEDIUM_FONT
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    # Once this working we create another label with all the initial specs
    main_group.pop()

    # Testing Color
    header_text_area.text = "Testing Color"
    text_initial_specs = bitmap_label.Label(
        MEDIUM_FONT,
        text="Circuit Python",
        x=display.width // 2,
        y=display.height // 2,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    text_initial_specs.color = 0x004400
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    # Testing Background Color
    header_text_area.text = "Testing Background Color"
    text_initial_specs = bitmap_label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    text_initial_specs.background_color = 0x990099
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    # Testing Background Color
    header_text_area.text = "Testing Background Tight"
    text_initial_specs = bitmap_label.Label(
        BIG_FONT,
        text="aaaaq~",
        x=0,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        background_tight=True,
    )
    main_group.append(text_initial_specs)
    text_initial_specs = bitmap_label.Label(
        BIG_FONT,
        text="aaaaq~",
        x=90,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        background_tight=False,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()
    main_group.pop()

    # Testing Padding
    header_text_area.text = "Testing Padding"
    text_initial_specs = bitmap_label.Label(
        BIG_FONT,
        text="CircuitPython",
        x=display.width // 4,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    # Testing Anchor Point/ Anchored Position
    header_text_area.text = "Testing Anchor Point/Anchored Position"
    text_initial_specs = bitmap_label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    try:
        text_initial_specs.anchored_position = (100, 100)
        text_initial_specs.anchor_point = (0.5, 0.5)

    except TypeError:
        print("Test is failing here")
        main_group.pop()
        warning_text = bitmap_label.Label(
            BIG_FONT,
            text="Test Fail",
            x=display.width // 2,
            y=display.height // 4,
            background_color=0x004499,
        )
        main_group.append(warning_text)
        time.sleep(TIME_PAUSE)
        display.show(main_group)

    main_group.pop()

    # Testing Scale
    header_text_area.text = "Testing Scale"
    text_initial_specs = bitmap_label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)

    text_initial_specs.scale = 2
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    # Testing Base Alignment
    header_text_area.text = "Testing Base Alignment"
    text_initial_specs = bitmap_label.Label(
        MEDIUM_FONT,
        text="python",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        base_alignment=True,
    )
    main_group.append(text_initial_specs)
    text_initial_specs = bitmap_label.Label(
        BIG_FONT,
        text="circuit",
        x=display.width // 2 - 100,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        base_alignment=True,
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()
    main_group.pop()

    # Testing Direction
    header_text_area.text = "Testing Direction-UPR"
    text_initial_specs = bitmap_label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
        label_direction="UPR",
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    header_text_area.text = "Testing Direction-DWR"
    text_initial_specs = bitmap_label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
        label_direction="DWR",
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    header_text_area.text = "Testing Direction-UPD"
    text_initial_specs = bitmap_label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
        label_direction="UPD",
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    header_text_area.text = "Testing Direction-RTL"
    text_initial_specs = bitmap_label.Label(
        MEDIUM_FONT,
        text="CircuitPython",
        x=display.width // 2,
        y=display.height // 2,
        color=0xFFFFFF,
        background_color=0x990099,
        padding_right=10,
        padding_top=10,
        padding_bottom=10,
        padding_left=10,
        anchored_position=(display.width // 2, display.height // 2),
        anchor_point=(0.5, 0.5),
        label_direction="RTL",
    )
    main_group.append(text_initial_specs)
    display.show(main_group)
    time.sleep(TIME_PAUSE)
    main_group.pop()

    text_area.text = "Finished"
    print("Tests finished")
