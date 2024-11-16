# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of setting the DAC value up and down through its entire range
# of values.

#basic board functions
import board
import busio
import digitalio
import analogio


#the DAC drivers
import adafruit_mcp4725

#for the random sampling
import math
import random

from enum import Enum

#Initializations

# Initialize I2C bus for the DAC
i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
# Initialize MCP4725 device
dac = adafruit_mcp4725.MCP4725(i2c)

#Initialize ADC input to double check the DAC is working as intended
adc = analogio.AnalogIn(board.GP28)


# Optionally you can specify a different addres if you override the A0 pin.
# amp = adafruit_max9744.MAX9744(i2c, address=0x63)

# There are a three ways to set the DAC output, you can use any of these:
dac.value = 65535  # Use the value property with a 16-bit number just like
# the AnalogOut class.  Note the MCP4725 is only a 12-bit
# DAC so quantization errors will occur.  The range of
# values is 0 (minimum/ground) to 65535 (maximum/Vout).

dac.raw_value = 4095  # Use the raw_value property to directly read and write
# the 12-bit DAC value.  The range of values is
# 0 (minimum/ground) to 4095 (maximum/Vout).

dac.normalized_value = 1.0  # Use the normalized_value property to set the
# output with a floating point value in the range
# 0 to 1.0 where 0 is minimum/ground and 1.0 is
# maximum/Vout.

#input pins for chess piece - not sure if I need pull downs here!!!!
def setPinsInput(pins):
    pin_objects = []
    for pin in pins:
        dio = digitalio.DigitalInOut(pin)
        dio.direction = digitalio.Direction.INPUT
        #dio.pull = digitalio.Pull.DOWN  # Use PULL.UP or PULL.DOWN as needed
        pin_objects.append(dio)

    return pin_objects

letter_pins = setPinsInput([board.GP21, board.GP20, board.GP19])
number_pins = setPinsInput([board.GP18, board.GP17, board.GP16])


#helper functions

#guassian stuff - Marsaglia Polar method
def get_standard_normal_sample():
    """Using the Marasaglia Polar method"""
    while True:
        u = random.uniform(-1, 1)
        v = random.uniform(-1, 1)
        s = u * u + v * v
        if s >= 1: #check if in unit circle, clever
            continue
        return u * math.sqrt(-2 * math.log(s) / s)

def get_scaled_gaussian_sample(mean, standard_deviation):
    return get_standard_normal_sample() * standard_deviation + mean

#getting the chessboard number
def get_binary(pins):
    value = 0
    for i, pin in enumerate(reversed(pins))
        if pin.value:
            value |= (1 << i)
    return value


def read_chess_piece():
    nums_to_let = ["A","B","C","D","H","G","F","E"]

    letter = nums_to_let[get_binary(letter_pins)]

    number = get_binary(number_pins)

    return letter + str(number)

#for the state machine
#Fault types:
    #placement
    #sensor failure
    #ect
#we can include other settings here such as how many sensors to simulate?

class failure_mode(Enum):
    PLACEMENT = 1
    SENSOR = 2
    OTHER = 3

FAILURE_MODE = failure_mode.PLACEMENT

# Main loop
print(f"Simulation beggining with failure mode {FAILURE_MODE}.")

while True:
    #read in the inputs


    #simulate failure mode
    match FAILURE_MODE:
        case failure_mode.PLACEMENT:
            pass
        case _:
            pass
    # Go up the 12-bit raw range.
    #print("Going up 0-3.3V...")
    #for i in range(4095):
        #dac.raw_value = i
        #print(f"Reading: {adc.value}")
    # Go back down the 12-bit raw range.
    #print("Going down 3.3-0V...")
    #for i in range(4095, -1, -1):
        #dac.raw_value = i
        #print(f"Reading: {adc.value}")



