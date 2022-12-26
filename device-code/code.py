import adafruit_gps
import board
import busio
import digitalio
import time
import directory_functions

# Setup/Define a bunch of stuff.
RX = board.GP13
TX = board.GP12
uart = busio.UART(TX, RX, baudrate=9600, timeout=30)
gps = adafruit_gps.GPS(uart, debug=False)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

## This was just a quick test to show storing code on the sd card and running it.
## Just keeping it around for reference.
#import hellodave
#with open("/sd/hellodave.py", "w") as f:
#    f.write("print('Hello big davey boy')")

# Mount the SD card and print its contents
directory_functions.mount_sd_card()
directory_functions.print_directory("/sd")

def _format_datetime(datetime):
    return "{:02}/{:02}/{} {:02}:{:02}:{:02}".format(
        datetime.tm_mon,
        datetime.tm_mday,
        datetime.tm_year,
        datetime.tm_hour,
        datetime.tm_min,
        datetime.tm_sec,
    )

def flash_led():
    if led.value == True:
        led.value = False
    else:
        led.value = True

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()
count = 0

## Print out a GPS log to make sure we are writing it ok
#with open("/sd/gps_log.log", "rt") as f:
#    data = f.read()
#    print(data)

filename = directory_functions.get_next_logfilename("/sd", "gps_logfile")
print("Got filename: " + filename)

with open(filename, "w") as f:
    while True:
        gps.update()
        current = time.monotonic()

        if current - last_print >= 1.0:
            # Flash the LED once every second so we know we are running
            flash_led() # TODO - Flash NeoPixel Green

            last_print = current
            if not gps.has_fix:
                # TODO - Flash NeoPixel Red
                print(str(count))
                count = count + 1
                print('Waiting for fix...')
                continue

            local_time = time.localtime()
            print('=' * 40)
            f.write('=' * 40)

            print(
                "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                    gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                    gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    gps.timestamp_utc.tm_min,  # month!
                    gps.timestamp_utc.tm_sec,
                )
            )
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
            count = 0
