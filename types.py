from enum import Enum

#state of the simulator
#Fault types:
    #placement
    #sensor failure
    #ect
#we can include other settings here such as how many sensors to simulate?

class failure_mode(Enum):
    STOP = 0
    PLACEMENT = 1
    SENSOR = 2
    OTHER = 3



class piece_type(Enum):
    EMPTY = 0
    PAWN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class polarity(Enum):
    BLACK = 0
    WHITE = 1
