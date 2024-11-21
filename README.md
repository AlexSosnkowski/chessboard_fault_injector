# Welcome

This is a simulator for a Hall effect digital chessboard. It injects faults into the micocontroller for the chessboard by simulating the analog readings of the Hall effect sensors through a dac.

This uses ciruit python.

There are a few relevant files. Mainly, the code.py is the main code file that is put onto the board.

# Testing board / serial connection

Commands needed to connect to the device

to find device (probably AM0, AM1, ...)

"ls /dev/tty*"

to connect to the board through serial usb

"screen /dev/ttyACM4 115200"

This should then recieve anything sent with print()
REPL can also be entered to quickly test code snipets like normal python REPL
Crtl+D reloads it

# Mappings

Below are the input mappings (from the chess board MCU) for what piece
Chess piece:

    a_1 a_2 a_3
    000->A
    001->B
    010->C 
    011->D
    100->H
    101->G
    110->F
    111->E

The three bits for row selection are just the numbers b_1 b_2 b_3
e.g 000->1...111->7.


The pins on the Pi Pico 2 for this are:

    3 pins for letter:
        a_1 = GP21 - white
        a_2 = GP20 - grey
        a_3 = gp19 - purple

    3 pins for number:
        b_1 = GP18 - blue
        b_2 = GP17 - green
        b_3 = GP16 - yellow 




# To Do

Read in from the input pins, calculate dac value, output it, reset. 

Should there be a way to communicate that the controller should change to a new piece or has finished proccessing the new piece? Timing errors?

Implement various modes of failure. 

More details:

1) double check that this is the correct way to handle displacement outputs on the DAC
2) code in other faults and / or dual or triple redundant sensor systems
3) can we code in other sensor failures (i.e sensor randomly breaks with a poisson distribution)
4) How can we communicate what the ground truth piece should be (i2c or serial, ect.) or can the other MCU assume a ground truth of default board layout?
Lots of testing

# Links

[Circuit Python Docs](https://docs.circuitpython.org/en/latest/README.html)

[Sensor Readings](https://docs.google.com/spreadsheets/d/1cUmQfoy8K9V3ad0Eh1IIA8iruwVh9r83LEivc1fVg_w/edit?gid=0#gid=0)

[Guassian Sampling](https://orionrobots.co.uk/2022/10/23/gaussian-circuitpython.html)
