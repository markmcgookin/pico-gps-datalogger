import adafruit_gps
import board
import busio
import digitalio
import os
import sdcardio
import storage
import sys
import time

RX = board.GP13
TX = board.GP12

uart = busio.UART(TX, RX, baudrate=9600, timeout=30)
gps = adafruit_gps.GPS(uart, debug=False)

spi = busio.SPI(board.GP2, board.GP3, board.GP4)
cs = board.GP5

sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)# Write your code here :-)

storage.mount(vfs, "/sd")
sys.path.append("/sd")

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def print_directory(path, tabs=0):
    for file in os.listdir(path):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000

        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)

        prettyprintname = ""
        for _ in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

        # recursively print directory contents
        if isdir:
            print_directory(path + "/" + file, tabs + 1)
            
def _format_datetime(datetime):
    return "{:02}/{:02}/{} {:02}:{:02}:{:02}".format(
        datetime.tm_mon,
        datetime.tm_mday,
        datetime.tm_year,
        datetime.tm_hour,
        datetime.tm_min,
        datetime.tm_sec,
    )

print("Files on filesystem:")
print("=====================")

print_directory("/sd")

import hellodave

#with open("/sd/hellodave.py", "w") as f:
#    f.write("print('Hello big davey boy')")

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()
count = 0
led_on = True
while True:

    gps.update()

    current = time.monotonic()
    if current - last_print >= 1.0:
        
        if led_on:
            led.value = False
            led_on = False
        else:
            led.value = True
            led_on = True
        
        last_print = current
        if not gps.has_fix:
            print(str(count))
            count = count + 1
            print('Waiting for fix...')
            continue

        local_time = time.localtime()            
        print('=' * 40)  # Print a separator line.
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        print('Local time: {}'.format(_format_datetime(local_time)))
        
        with open("/sd/gps_log.log", "w") as f:
            f.write('Latitude: {0:.6f} degrees'.format(gps.latitude))
            f.write('Longitude: {0:.6f} degrees'.format(gps.longitude))
            f.write('Local time: {}'.format(_format_datetime(local_time)))

        count = 0


