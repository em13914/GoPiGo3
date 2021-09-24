#!/usr/bin/env python

"""
Simplified version for DVC senior robotics students
"""

from easygopigo3 import EasyGoPiGo3
from gopigo3 import FirmwareVersionError
import sys
import signal
from time import sleep

ERROR = 0 # the error that's returned when the DistanceSensor is not found

# used for stopping the while loop that's in the Main() function
robot_operating = True

def signal_handler(signal, frame):
    global robot_operating
    print("CTRL-C combination pressed")
    robot_operating = False

# the function that runs immediately once you load this script
def Main():

    print("   _____       _____ _  _____         ____  ")
    print("  / ____|     |  __ (_)/ ____|       |___ \ ")
    print(" | |  __  ___ | |__) || |  __  ___     __) |")
    print(" | | |_ |/ _ \|  ___/ | | |_ |/ _ \   |__ < ")
    print(" | |__| | (_) | |   | | |__| | (_) |  ___) |")
    print("  \_____|\___/|_|   |_|\_____|\___/  |____/ ")
    print("                                            ")

    # initializing an EasyGoPiGo3 object and a DistanceSensor object
    # used for interfacing with the GoPiGo3 and with the distance sensor
    try:
        gopigo3 = EasyGoPiGo3()
        distance_sensor = gopigo3.init_distance_sensor()

    except IOError as msg:
        print("GoPiGo3 robot not detected or DistanceSensor not installed.")
        debug(msg)
        sys.exit(1)

    global robot_operating

    # while the script is running
    while robot_operating:
        determined_speed = 0

        # CHECK IF SENSOR CAN'T BE FOUND
        if distance_sensor.read_mm() == ERROR:
            print("Cannot reach DistanceSensor. Stopping the process.")
            robot_operating = False

        # CHECK IF THE ROBOT IS SUPER CLOSE TO AN OBSTACLE
        elif distance_sensor.read_mm() < 250:
            # stop the GoPiGo
            gopigo3.set_speed(1) #for some reason set_speed(0) sets the speed to max?!
            print("250mmm or less!")

        elif distance_sensor.read_mm() < 500:
            # slow down the GoPiGo
            gopigo3.set_speed(100)
            print("500mm or less!")
            
        elif distance_sensor.read_mm() < 750:
            # slow down the GoPiGo
            gopigo3.set_speed(200)
            print("750mm or less!")

        else:
            # set the robot to full speed because the coast is clear
            gopigo3.set_speed(300)
            print("Coast is clear!")
        
        # DO THESE THINGS BEFORE STARTING THE LOOP OVER
        gopigo3.forward()
        gopigo3.close_eyes()
        gopigo3.led_off(0)
        gopigo3.led_off(1)
        print("Current distance : {:4} mm Current speed: {:4} ".format(distance_sensor.read_mm(), gopigo3.get_speed()))
        sleep(0.08)

    # and finally stop the GoPiGo3 from moving
    gopigo3.stop()


if __name__ == "__main__":
    # signal handler
    # handles the CTRL-C combination of keys
    signal.signal(signal.SIGINT, signal_handler)
    Main()
