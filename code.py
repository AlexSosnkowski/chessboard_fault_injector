# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of setting the DAC value up and down through its entire range
# of values.

#enums like chess board pieces, ect.
from types import *

#basic board functions
import board
import busio
import digitalio
import analogio
import time


#the DAC drivers
import adafruit_mcp4725

#for the random sampling
import math
import random


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
#dac.value = 65535  # Use the value property with a 16-bit number just like
# the AnalogOut class.  Note the MCP4725 is only a 12-bit
# DAC so quantization errors will occur.  The range of
# values is 0 (minimum/ground) to 65535 (maximum/Vout).

#dac.raw_value = 4095  # Use the raw_value property to directly read and write
# the 12-bit DAC value.  The range of values is
# 0 (minimum/ground) to 4095 (maximum/Vout).

#dac.normalized_value = 1.0  # Use the normalized_value property to set the
# output with a floating point value in the range
# 0 to 1.0 where 0 is minimum/ground and 1.0 is
# maximum/Vout.

#set dac to zero
dac.normalized_value = 0.0

#input pins for chess piece - not sure if I need pull downs here!!!!
def setPinsInput(pins):
    pin_objects = []
    for pin in pins:
        dio = digitalio.DigitalInOut(pin)
        dio.direction = digitalio.Direction.INPUT
        #dio.pull = digitalio.Pull.DOWN  # Use PULL.UP or PULL.DOWN as needed
        pin_objects.append(dio)

    return pin_objects
# a1 a2 a3
letter_pins = setPinsInput([board.GP21, board.GP20, board.GP19])
# b1 b2 b3
number_pins = setPinsInput([board.GP18, board.GP17, board.GP16])


#helper functions

def constrain(value, min_value, max_value):
    return max(min(value, max_value), min_value)

#guassian stuff - Marsaglia Polar method
#https://orionrobots.co.uk/2022/10/23/gaussian-circuitpython.html
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
    for i, pin in enumerate(reversed(pins)):
        if pin.value:
            value |= (1 << i)
    return value


def read_board_position():
    nums_to_let = ["A","B","C","D","H","G","F","E"]

    letter = nums_to_let[get_binary(letter_pins)]

    number = get_binary(number_pins)

    return letter + "_" +  str(number)

#this assumes a default board setup
#not great but maybe more memory efficent than a big matrix of pieces
def read_board_piece(pos):
    pos = pos.split("_")
    letter = pos[0]
    number = int(pos[1])

    if number <= 2:
        polar = polarity.WHITE
    else:
        polar = polarity.BLACK

    if number == 2 or number == 7:
        piece = piece_type.PAWN
    else:
        if letter in ("A", "H"):
            piece = piece_type.ROOK
        elif letter in ("B", "G"):
            piece = piece_type.KNIGHT
        elif letter in ("C", "F"):
            piece = piece_type.BISHOP
        elif letter == "D":
            piece = piece_type.QUEEN
        elif letter == "E":
            piece = piece_type.KING
        else:
            piece = piece_type.EMPTY

    #1) piece type 2) polarity (white or black)
    return (piece, polar)

#get the adc reading

#double check this table and also convert it into another file later
READING_VALUES = {
    piece_type.EMPTY: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], # this seems wrong
    piece_type.PAWN: [16383.0 / 16383.0, 16383.0 / 16383.0, 16186.0 / 16383.0, 16186.0 / 16383.0, 15988.0 / 16383.0, 10659.0 / 16383.0, 7698.0 / 16383.0, 7106.0  / 16383.0],
    piece_type.BISHOP: [15001.0  / 16383.0, 15001.0  / 16383.0, 14804.0  / 16383.0, 13225.0  / 16383.0, 12041.0  / 16383.0, 10264.0  / 16383.0, 9277.0  / 16383.0, 8685.0  / 16383.0],
    piece_type.KNIGHT: [13225.0  / 16383.0, 12633.0  / 16383.0, 12238.0  / 16383.0, 12041.0  / 16383.0, 11448.0  / 16383.0, 10659.0  / 16383.0, 9475.0  / 16383.0, 8882.0  / 16383.0],
    piece_type.ROOK: [11843.0  / 16383.0, 11646.0  / 16383.0, 11448.0  / 16383.0, 11054.0  / 16383.0, 10461.0  / 16383.0, 9869.0  / 16383.0, 9277.0  / 16383.0, 8685.0  / 16383.0],
    piece_type.QUEEN: [10264.0  / 16383.0, 10264.0  / 16383.0, 10067.0  / 16383.0, 9869.0  / 16383.0, 9475.0  / 16383.0, 9277.0  / 16383.0, 9080.0  / 16383.0, 8685.0  / 16383.0],
    piece_type.KING: [8833.0  / 16383.0, 8784.0  / 16383.0, 8586.0  / 16383.0, 8488.0  / 16383.0, 8389.0  / 16383.0, 8340.0  / 16383.0, 8241.0  / 16383.0, 8192.0  / 16383.0],
}

#alter the noise level by increasing the std
def get_DAC_output(piece, polar, std=1.0):

    bins = READING_VALUES[piece]

    #the noise
    displacement = get_scaled_gaussian_sample(0.0, std)

    b = constrain(int(displacement), 0, len(bins) - 1)

    if b == len(bins) - 1:
        print("this shouldn't happen realistically")
        return bins[b]
    else:
        #do a interpolation between the bins
        v_1 = bins[b]; v_2 = bins[b+1]
        output = v_1 + (displacement - float(b)) * (v_2 - v_1)
        if output > 1.0:
            print("panic!")
        print("d", displacement, "v1", v_1, "v_2", v_2)
        #output = constrain(output, 0.0, 1.0)
        #flip if polarity
        if polar == polarity.WHITE:
            return output
        else:
            return 1.0 - output






#SETTINGS !!!!!
FAILURE_MODE = failure_mode.PLACEMENT
STD_DEV = 1.0

# Main loop
print(f"Simulation beggining with failure mode {FAILURE_MODE}.")
prev_place = ""

while True:
    curr_place = read_board_position
    if curr_place == prev_place:
        continue
    else:
        prev_place = curr_place
    #read in the inputs
    #position = read_board_position()
    #simulate failure mode

    #testing
    #example = (piece_type.PAWN, polarity.WHITE)
    #print(get_DAC_output(*example))
    #time.sleep(0.5)

    if FAILURE_MODE == failure_mode.PLACEMENT:
        p = read_board_piece(curr_place)
        dac.normalized_value = get_DAC_output(p, STD_DEV)
    else:
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



