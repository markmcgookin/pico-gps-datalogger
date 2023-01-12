import board
import busio
import digitalio
import os
import time

def print_directory(path, tabs=0):
    print("Files on filesystem:")
    print("=====================")
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

def file_exists(filename):
    file_exists = False
    try:
        os.stat(filename)
        file_exists = True
    except OSError:
        file_exists = False
    return file_exists

def get_next_logfilename(path, filename):
    count = 1
    while True:
        newfilename = path + "/" + filename + "_" + str(count) + ".log"
        print("Checking for " + newfilename)
        if not file_exists(newfilename):
            return newfilename
        else:
            count = count + 1

def log_gps_data(gps, filename):
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
