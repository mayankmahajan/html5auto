import math
import numpy
import cmath

NUM_SIGNIFICAND_BITS = 10
SIGNIFICAND_MASK = (1 << NUM_SIGNIFICAND_BITS) - 1
MAX_SIGNIFICAND_NUM = SIGNIFICAND_MASK
LOG10_MAX_SIGNIFICAND = math.log10(SIGNIFICAND_MASK)
NUM_EXPONENT_BITS = 5
EXPONENT_MASK = ((1 << NUM_EXPONENT_BITS) - 1) << NUM_SIGNIFICAND_BITS
EXPONENT_BIAS = 1 << (NUM_EXPONENT_BITS - 1)
MIN_EXPONENT_NUM = -EXPONENT_BIAS
MAX_EXPONENT_NUM = EXPONENT_BIAS - 1
BASE = 10
SIGNBIT_MASK = 0 << (NUM_SIGNIFICAND_BITS + NUM_EXPONENT_BITS)

MIN_FLOAT_VALUE = float(-MAX_SIGNIFICAND_NUM * math.pow(BASE, MAX_EXPONENT_NUM))
MAX_FLOAT_VALUE = float(MAX_SIGNIFICAND_NUM * math.pow(BASE, MAX_EXPONENT_NUM))
MIN_NORMAL_VALUE = float(math.pow(BASE, MIN_EXPONENT_NUM))

# print MAX_EXPONENT_NUM - MIN_EXPONENT_NUM + 2
POWER_OF_TENS =[]
# (1054035, 37921)
for i in range(MAX_EXPONENT_NUM - MIN_EXPONENT_NUM + 2):
    POWER_OF_TENS.append(float(math.pow(BASE, MIN_EXPONENT_NUM + i)))


def floatBitsToShort(number): # float number
    if number > MAX_FLOAT_VALUE:
        number = MAX_FLOAT_VALUE
    elif number < MIN_NORMAL_VALUE and number > 0:
        number = MIN_NORMAL_VALUE
    elif number < MIN_FLOAT_VALUE:
        number = MIN_FLOAT_VALUE
    # compress it
    return compress(float(number))

def compress(number): # float number
    if number == 0:
        return 0
    exponent = 0
    mantissa = 0
    tempnumber = number
    delta = float(math.ceil(math.log10(tempnumber)- LOG10_MAX_SIGNIFICAND))
    # delta = (float) Math.ceil(Math.log10(tempnumber) - LOG10_MAX_SIGNIFICAND);
    if delta < -16:
        diff = float(-16 - delta)
        add = int(diff)
        if diff != add:
            add+=1
        delta += add
    exponent = int(delta + EXPONENT_BIAS)
    tempnumber = tempnumber * POWER_OF_TENS[int((EXPONENT_BIAS - delta))];
    mantissa = int(round(tempnumber))
    return numpy.ushort(((SIGNBIT_MASK) | ((exponent << NUM_SIGNIFICAND_BITS) & EXPONENT_MASK) | (mantissa & SIGNIFICAND_MASK)))


# compressedNumber =1054035
def shortBitsToFloat(compressedNumber):  # short  compressedNumber

	mantissa = (compressedNumber & SIGNIFICAND_MASK)
	exponent = ((compressedNumber & EXPONENT_MASK) >> NUM_SIGNIFICAND_BITS) - EXPONENT_BIAS
	return (mantissa * math.pow(BASE, exponent))
# (1054035, 37921)
# compressedNumber = floatBitsToShort(9223372036854770000)
# print compressedNumber
# print shortBitsToFloat(compressedNumber)