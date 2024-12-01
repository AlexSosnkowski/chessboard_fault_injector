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

#Initialize position displacements interpolations
position_displacments = {}
Bishop_interp = [11843,11829.1035549801,11815.2021004983,11801.2956392393,11787.3841738879,11773.4677071289,11759.5462416472,11745.6197801275,11731.6883252547,11717.7518797135,11703.8104461888,11689.8640273654,11675.912625928,11661.9562445615,11647.9948859507,11634.2530020762,11621.0315978146,1608.1994005024,11595.6184334559,11583.1507199915,11570.6582834255,11558.0031470743,11545.0473342541,11531.6528682813,1517.6817724723,11502.9960701434,11487.457784611,11470.9289391913,11453.2715572007,11434.2329167033,11413.4789136661,11391.0960258371,11367.1924393586,11341.8763403728,1315.2559150221,11287.4393494487,11258.5348297951,11228.6505422034,11197.894672816,11166.3754077752,11134.2009332233,1101.4794353026,11068.3191001555,11034.4879013327,10998.6020845315,10960.7204469582,10921.0976390012,10879.9883110492,10837.6471134905,10794.3286967136,10750.2877111071,10705.7788070593,10661.0566349589,10616.3758451941,10571.9910881536,10528.1570142259,10485.1282737993,10443.0463709288,0401.1612373319,10359.2845805584,10317.4153410052,10275.5524590695,10233.6948751484,10191.8415296389,10149.9913629381,0108.1433154432,10066.2963275512,10024.4493396592,9982.60129216422,9940.75112546347,9898.89777995397,9857.0404040404,9815.18181818182,9773.32323232323,9731.46464646465,689.60606060606,9647.74747474748,9605.88888888889,9564.0303030303,9522.17171717172,9480.31313131313,9438.45454545455,396.59595959596,9354.73737373737,9312.87878787879,9271.0202020202,9229.16161616162,9187.30303030303,9145.44444444445,9103.58585858586,9061.72727272727,9019.86868686869,8978.0101010101,8936.15151515151,8894.29292929293,8852.43434343434,8810.57575757576,8768.71717171717,8726.85858585859,8685]
King_interp = [8833, 8832.66470092175, 8831.68629362309, 8830.10601300814, 8827.96509398103, 8825.30477144586, 8822.16628030678, 8818.59085546789, 8814.61973183332, 8810.29414430719, 8805.65532779363, 8800.74451719676, 8795.60294742069, 8790.27185336956, 8784.79246994748, 8778.15720776486, 8768.83360379373, 8757.18653191061, 8743.61120400355, 8728.50283196057, 8712.25662766971, 8695.267803019, 8677.93156989648, 8660.64314019019, 8643.79772578816, 8627.79053857842, 8613.01679044901, 8599.87169328796, 8588.75045898331, 8579.54421968828, 8571.02844273755, 8563.0575448955, 8555.56024889282, 8548.4652774602, 8541.70135332832, 8535.19719922788, 8528.88153788955, 8522.68309204403, 8516.53058442201, 8510.35273775417, 8504.07827477121, 8497.6359182038, 8490.95439078264, 8483.96630295046, 8476.67708486829, 8469.15654178322, 8461.47667828363, 8453.70949895792, 8445.92700839448, 8438.20121118168, 8430.60411190791, 8423.20771516157, 8416.08402553103, 8409.30504760469, 8402.94278597094, 8397.06924521814, 8391.75642993471, 8387.0581956863, 8382.8509618782, 8379.03998165737, 8375.55503286908, 8372.32589335865, 8369.28234097135, 8366.3541535525, 8363.47110894739, 8360.56298500131, 8357.55955955956, 8354.39061046744, 8350.98591557024, 8347.27525271327, 8343.18839974181, 8338.63527715043, 8333.26155907974, 8327.06697882455, 8320.19341379947, 8312.78274141911, 8304.97683909805, 8296.91758425092, 8288.74685429231, 8280.60652663683, 8272.63847869908, 8264.98458789368, 8257.78673163522, 8251.1867873383, 8245.32663241754, 8240.33867381587, 8235.76010490274, 8231.28308172936, 8226.9255181107, 8222.70532786174, 8218.64042479745, 8214.74872273281, 8211.04813548278, 8207.55657686236, 8204.29196068651, 8201.27220077021, 8198.51521092843, 8196.03890497616, 8193.86119672835, 8192]
Knight_interp = [13225, 13176.5778768757, 13128.9857714474, 13082.2653826624, 13036.4584094678, 12991.606550811, 12947.7515056392, 12904.9349728996, 12863.1986515394, 12822.584240506, 12783.1334387465, 12744.8879452081, 12707.8894588382, 12672.179678584, 12637.8003033926, 12604.388203007, 12571.340095299, 12538.7574812961, 12506.7533497635, 12475.4406894666, 12444.9324891706, 12415.341737641, 12386.7814236429, 12359.3645359417, 12333.2040633027, 12308.4129944913, 12285.1043182728, 12263.3910234124, 12243.3860986755, 12225.2896101981, 12209.2285039616, 12194.873804341, 12181.8763151005, 12169.8868400046, 12158.5561828174, 12147.5351473034, 12136.4745372268, 12125.0251563521, 12112.8378084434, 12099.5632972653, 12084.8524265818, 12068.3560001575, 12049.7248217566, 12028.2313687099, 12002.1301110096, 11971.6357997147, 11937.2005236369, 11899.2763715882, 11858.3154323804, 11814.7697948254, 11769.0915477351, 11721.7327799214, 11673.145580196, 11623.7820373709, 11574.094240258, 11524.5342776691, 11475.554238416, 11427.4200402088, 11378.8867158178, 11329.5555189045, 11279.3287537308, 11228.1087245586, 11175.7977356497, 11122.298091266, 11067.5120956694, 11011.3420531217, 10953.6902678848, 10894.4590442206, 10833.5506863909, 10770.8674986576, 10706.3117852825, 10639.5205050311, 10566.2142909653, 10485.9506168495, 10400.0674456204, 10309.9027402149, 10216.7944635697, 10122.0805786214, 10027.0990483069, 9933.18783556294, 9841.68490332621, 9753.92821453348, 9671.2557321215, 9595.00541902702, 9526.51523818678, 9467.02815893027, 9411.84165330555, 9357.88270723062, 9305.35976850983, 9254.48128494755, 9205.45570434811, 9158.49147451589, 9113.79704325522, 9071.58085837047, 9032.05136766598, 8995.41701894612, 8961.88626001524, 8931.66753867769, 8904.96930273783, 8882]
Pawn_interp = [6383, 16383, 16383, 16383, 16383, 16383, 16383, 16383, 16383, 16383, 16383, 16383, 16383, 16383, 16383, 16380.9169101483, 16373.7014198716, 16362.1284954432, 16347.033809166, 16329.2530333433, 16309.6218402781, 16288.9759022734, 16268.1508916324, 16247.982480658, 16229.3063416534, 16212.9581469217, 16199.7735687659, 16190.5882794891, 16186.2379513944, 16186, 16186, 16186, 16186, 16186, 16186, 16186, 16186, 16186, 16186, 16186, 16186, 16186, 16186, 16185.654544358, 16183.3998753593, 16179.0708423113, 16172.6975344178, 16164.3100408829, 16153.9384509104, 16141.6128537044, 16127.3633384688, 16111.2199944076, 16093.2129107248, 16073.3721766242, 16051.7278813099, 16028.3101139859, 16003.148963856, 15966.1263683453, 15839.6165892223, 15618.5549035949, 15316.662860764, 14947.6620100303, 14525.2739006947, 14063.2200820581, 13575.2221034212, 13075.0015140849, 12576.27986335, 12092.7787005175, 11638.219574888, 11226.3240357624, 10870.8136324415, 10581.9889662825, 10311.4392428239, 10041.1403117082, 9773.48567817411, 9510.86884745992, 9255.68332480413, 9010.32261544522, 8777.18022462165, 8558.64965757188, 8357.12441953437, 8174.99801574759, 8014.66395145001, 7878.51573188008, 7768.94686227628, 7688.05345767433, 7619.65827158236, 7553.71552856897, 7490.64365398433, 7430.86107317861, 7374.78621150199, 7322.83749430464, 7275.43334693672, 7232.99219474842, 7195.93246308989, 7164.67257731132, 7139.63096276288, 7121.22604479473, 7109.87624875704, 7106]
Queen_interp = [10264, 10264, 10264, 10264, 10264, 10264, 10264, 10264, 10264, 10264, 10264, 10264, 10264, 10264, 10264, 10262.5983761315, 10257.6597312813, 10249.5604921782, 10238.7174371606, 10225.5473445671, 10210.4669927361, 10193.8931600061, 10176.2426247157, 10157.9321652033, 10139.3785598074, 10120.9985868665, 10103.2090247191, 10086.4266517038, 10071.0682461589, 10057.1815913972, 10043.89332274, 10031.0139719871, 10018.4055624547, 10005.9301174592, 9993.44966031694, 9980.8262143442, 9967.92180285736, 9954.59844917275, 9940.71817660671, 9926.14300847557, 9910.73496809569, 9894.35607878339, 9876.86836385502, 9857.72970580286, 9835.2427612798, 9809.71238857189, 9781.69193825821, 9751.7347609178, 9720.39420712974, 9688.22362747309, 9655.77637252691, 9623.60579287026, 9592.2652390822, 9562.30806174179, 9534.28761142811, 9508.7572387202, 9486.27029419714, 9467.13163614498, 9449.64392121661, 9433.26503190431, 9417.85699152443, 9403.28182339329, 9389.40155082725, 9376.07819714264, 9363.1737856558, 9350.55033968306, 9338.06988254077, 9325.59443754526, 9312.98602801288, 9300.10667725996, 9286.81840860284, 9273.0368768426, 9259.54846860812, 9246.54781429146, 9233.89410682617, 9221.44653914583, 9209.06430418401, 9196.60659487429, 9183.93260415024, 9170.90152494543, 9157.37255019344, 9143.20487282782, 9128.25768578217, 9112.39018199005, 9095.46155438503, 9077.32773682774, 9057.69505869506, 9036.49058149058, 9013.78453453453, 8989.64714714715, 8964.14864864865, 8937.35926835927, 8909.34923559923, 8880.18877968878, 8849.94812994813, 8818.69751569751, 8786.50716625717, 8753.44731094731, 8719.58817908818, 8685]
Rook_interp = [15001, 15001, 15001, 15001, 15001, 15001, 15001, 15001, 15001, 15001, 15001, 15001, 15001, 15001, 15001, 15000.1256010581, 14996.9484669693, 14991.5366892154, 14983.9829634292, 14974.3799852435, 14962.8204502909, 14949.3970542042, 14934.2024926161, 14917.3294611592, 14898.8706554664, 14878.9187711703, 14857.5665039036, 14834.9065492991, 14811.0316029895, 14779.6515915118, 14724.7083166476, 14648.2246835252, 14553.2855500182, 14442.9757740006, 14320.3802133462, 14188.5837259288, 14050.6711696223, 13909.7274023006, 13768.8372818374, 13631.0856661067, 13499.5574129822, 13377.3373803378, 13267.5104260474, 13171.235551328, 13081.1865301633, 12995.5389473409, 12913.4308616374, 12834.0003318292, 12756.385416693, 12679.7241750053, 12603.1546655426, 12525.8149470814, 12446.8430783983, 12365.3771182698, 12280.5551254724, 12191.5151587827, 12097.3952769773, 11996.8398167765, 11885.8985327123, 11765.3791534432, 11637.113748561, 11502.9343876575, 11364.6731403244, 11224.1620761535, 11083.2332647364, 10943.7187756651, 10807.4506785311, 10676.2610429263, 10551.9819384424, 10436.4454346711, 10331.4836012042, 10238.4907811315, 10151.2229411699, 10067.0317766588, 9985.84263755063, 9907.58087379805, 9832.17183535359, 9759.54087216982, 9689.6133341993, 9622.31457139459, 9557.56993370825, 9495.30477109285, 9435.44443350094, 9377.91427088509, 9322.63963319786, 9269.53442579563, 9217.86494014846, 9167.30198896905, 9117.95036274282, 9069.91485195522, 9023.30024709169, 8978.21133863765, 8934.75291707856, 8893.02977289984, 8853.14669658694, 8815.2084786253, 8779.31990950034, 8745.58577969751, 8714.11087970226, 8685]
POSITION_DISPLACMENTS = {
    piece_type.EMPTY: [16383/2], 
    piece_type.PAWN: Pawn_interp,
    piece_type.BISHOP: Bishop_interp,
    piece_type.KNIGHT: knight_interp,
    piece_type.ROOK: rook_interp,
    piece_type.QUEEN: queen_interp,
    piece_type.KING: king_interp 
}

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
# c1 c2
sensor_select_pins = setPinsInput([board.GP26, board.GP22])


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

    number = get_binary(number_pins) + 1

    # 0 would be a centrally located sensor, 1,2,3 are for triple sensor systems
    sensor_sel = get_binary(sensor_select_pins)

    return letter + "_" +  str(number) + "_" + str(sensor_sel)

#this assumes a default board setup
#not great but maybe more memory efficent than a big matrix of pieces
def read_board_piece(pos):
    #pos = pos.split("_")
    #letter = pos[0]
    #number = int(pos[1])
    letter = pos[0]
    number = int(pos[2])
    select = int(pos[4])
    if number <= 2:
        polar = polarity.WHITE
    else:
        polar = polarity.BLACK

    if number == 2 or number == 7:
        piece = piece_type.PAWN
    elif number == 1 or number == 8:
        if letter in ("A", "H"):
            piece = piece_type.ROOK
        elif letter in ("B", "G"):
            piece = piece_type.KNIGHT
        elif letter in ("C", "F"):
            piece = piece_type.BISHOP
        elif letter == "D":
            piece = piece_type.QUEEN
        else:
            piece = piece_type.KING
    else:
        piece = piece_type.EMPTY

    sensor_disp_from_center = (0, 0)
    # Calculated manually: assuming that the sensors have dimensions: 4.6x3.433 mm
    # A reasonable radial distance from the center is ~2.5 mm
    radial_disp = 2.5
    x_disp = 2.165 
    y_disp = 1.25 
    if select == 0:
       sensor-disp_from_center = (0, 0) 
    elif select == 1:
       sensor-disp_from_center = (0, radial_disp) 
    elif select == 2:
        sensor-disp_from_center = (-x_disp, -y_disp)
    elif select == 3:
        sensor-disp_from_center = (x_disp, -y_disp)

    #1) piece type 2) polarity (white or black) 3) the displacement from the center of the square
    return (piece, polar, sensor-disp_from_center)

#get the adc reading

#double check this table and also convert it into another file later
#READING_VALUES = {
#    piece_type.EMPTY: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], # this seems wrong
#    piece_type.PAWN: [16383.0 / 16383.0, 16383.0 / 16383.0, 16186.0 / 16383.0, 16186.0 / 16383.0, 15988.0 / 16383.0, 10659.0 / 16383.0, 7698.0 / 16383.0, 7106.0  / 16383.0],
#    piece_type.BISHOP: [15001.0  / 16383.0, 15001.0  / 16383.0, 14804.0  / 16383.0, 13225.0  / 16383.0, 12041.0  / 16383.0, 10264.0  / 16383.0, 9277.0  / 16383.0, 8685.0  / 16383.0],
#    piece_type.KNIGHT: [13225.0  / 16383.0, 12633.0  / 16383.0, 12238.0  / 16383.0, 12041.0  / 16383.0, 11448.0  / 16383.0, 10659.0  / 16383.0, 9475.0  / 16383.0, 8882.0  / 16383.0],
#    piece_type.ROOK: [11843.0  / 16383.0, 11646.0  / 16383.0, 11448.0  / 16383.0, 11054.0  / 16383.0, 10461.0  / 16383.0, 9869.0  / 16383.0, 9277.0  / 16383.0, 8685.0  / 16383.0],
#    piece_type.QUEEN: [10264.0  / 16383.0, 10264.0  / 16383.0, 10067.0  / 16383.0, 9869.0  / 16383.0, 9475.0  / 16383.0, 9277.0  / 16383.0, 9080.0  / 16383.0, 8685.0  / 16383.0],
#    piece_type.KING: [8833.0  / 16383.0, 8784.0  / 16383.0, 8586.0  / 16383.0, 8488.0  / 16383.0, 8389.0  / 16383.0, 8340.0  / 16383.0, 8241.0  / 16383.0, 8192.0  / 16383.0],
#}

#alter the noise level by increasing the std
def get_DAC_output(piece, polar, sensor_disp_from_center = (0,0), piece_disp_from_center = (0,0)):

    bins = POSITION_DISPLACMENTS[piece]

    total_position_displacment = (
        piece_disp_from_center[0]+sensor-disp_from_center[0], 
        piece_disp_from_center[1]+sensor-disp_from_center[1]
    )
    total_radial_displacement = constrain(((total_position_displacment[0])**2 + (total_position_displacment[1])**2)**0.5, 0.0, 7.0) / 7.0
    total_radial_displacement_bin_low = math.floor(total_radial_displacement)
    total_radial_displacement_bin_high = math.ciel(total_radial_displacement)

    #do a interpolation between the bins
    v_1 = bins[total_radial_displacement_bin_low]/16383; v_2 = bins[total_radial_displacement_bin_high]/16383
    output = v_1 + (total_radial_displacement - float(b)) * (v_2 - v_1)
    if output > 1.0:
        print("panic!")
    #print("d", displacement, "v1", v_1, "v_2", v_2)
    #output = constrain(output, 0.0, 1.0)
    #flip if polarity
    if polar == polarity.WHITE:
            return output
        else:
            return 1.0 - output






#SETTINGS !!!!!
FAILURE_MODE = failure_mode.PLACEMENT
POSIITON_DISP_STD_DEV = 2

# Main loop
print(f"Simulation beggining with failure mode {FAILURE_MODE}.")
prev_place = ""

while True:
    curr_place = read_board_position()
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
        curr_piece, curr_polarity, sensor_disp_from_center = read_board_piece(curr_place)

        # This code assumes that we are not moving any pieces... If a piece is moved, it's value in the map should be reset:
        # reset(position_displacements[curr_place])
        if SIMULATING_POSITION_DISPLACEMENT:
            if not (curr_place in position_displacments):
                posx_displacement = get_scaled_gaussian_sample(0.0, POSIITON_DISP_STD_DEV) 
                posy_displacement = get_scaled_gaussian_sample(0,0, POSIITON_DISP_STD_DEV)
                position_displacments[curr_place] = (posx_displacement, posy_displacement)

                output = get_DAC_output(piece=curr_piece, 
                    polar=curr_polarity, 
                    sensor_disp_from_center=sensor_disp_from_center, 
                    piece_disp_from_center=(posx_displacement, posy_displacement))
            else:
                output = get_DAC_output(piece=curr_piece, 
                    polar=curr_polarity, 
                    sensor_disp_from_center=sensor_disp_from_center, 
                    piece_disp_from_center=position_displacments[curr_place])
        else: 
            output = get_DAC_output(piece=curr_piece, 
                polar=curr_polarity, 
                sensor_disp_from_center=sensor_disp_from_center)

        dac.normalized_value = output
        print(curr_place)
        print("pin readings")
        for a in letter_pins + number_pins:
            print(a.value)
        print(f"We are at {curr_piece} with polarity {curr_polarity} and output {output}")
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



