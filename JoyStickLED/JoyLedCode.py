from signal import signal, SIGTERM, SIGHUP, pause
from time import sleep
from smbus2 import SMBus
from gpiozero import PWMLED

bus = SMBus(1)
#                   A0    A1    A2    A3    A4    A5    A6    A7
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)
# we are using A6 for y and A7 for x

#GPIO Pins for each LED
top = PWMLED(6)
right = PWMLED(26)
left = PWMLED(13)
bottom = PWMLED(19)

def safe_exit(signum, frame):
    exit(1)

# read the value on adc module
def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)

# stick drift is done seperately due to my joystick having irregular stick drift
# to get rid of stick drift for x axis
def no_drift_x(input):
    value = read_ads7830(input)
    
    if value > 175 or value < 130:
        return value
    else:
        return 127
    
# to get rid of stick drift for y axis
def no_drift_y(input):
    value = read_ads7830(input)
    
    if value > 90 or value < 75:
        return value
    else:
        return 127

# helps with making the movement of the joystick make the led brighter with more "force" applied in the direction
def read_min(input, axis):
    while (True):
        if(axis == "x"):
            value = no_drift_x(input)
        else:
            value = no_drift_y(input)

        yield (127-value)/127 if value < 110 else 0

def read_max(input, axis):
    while (True):
        if(axis == "x"):
            value = no_drift_x(input)
        else:
            value = no_drift_y(input)

        yield (value - 128)/127 if value > 140 else 0

try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    
    top.source    = read_min(6,"y") # 6 bc of y
    right.source  = read_min(7,"x") # 7 bc of x
    left.source   = read_max(7,"x") # 7 bc of x
    bottom.source = read_max(6,"y") # 6 bc of y
    
    sleep(0.1)
    pause()

except KeyboardInterrupt:
    pass

finally:
    # clear/clean up the leds so they shut down properly when program ends
    top.source = None
    top.close()
    right.source = None
    right.close()
    left.source = None
    left.close()
    bottom.source = None
    bottom.close()
