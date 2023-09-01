#   Calculator to do 4 
#   basic operations in 
#   GF(2⁸) mod x⁸ + x⁴ + x³ + x + 1
#   with coefficients over GF(2)
#
#   @author: Germán Rodríguez

IRREDUCTIBLE_POLY= 0b00011011 # x⁸ + x⁴ + x³ + x + 1

def add(num1, num2):
    return num1 ^ num2

def subtract(num1, num2):
    return num1 ^ num2

def mult(num1, num2):
    powers_num1 = get_powers_array(num1)
    return add_powers(powers_num1, num2)

def add_powers(powers_table, num):
    index = 0
    solution = 0
    while num != 0:
        if (num & 1) != 0:
            solution ^= powers_table[index]
        index += 1
        num >>= 1
    return solution

def get_powers_array(num):
    table = [num]
    for _ in range(7):
        num = mult_by_x(num)
        table.append(num)
    return table

def mult_by_x(num):
    # Extract bit 7 to see if it is a 1 or 0 
    bit_7 = (num >> 7) & 1
    # Left shift to num
    num <<= 1
    # If bit 8 is 1, turn to 0, doing an AND with bit 8 to 0
    num = 0xFF & num
    if bit_7 == 1:
        num ^= IRREDUCTIBLE_POLY
    return num

# Div is multiply by his multiplicative inverse 
def div(num1, num2):
    mi = multiplicative_inverse(num2)
    return mult(num1,mi)

def multiplicative_inverse(num):
    for i in range(1,256):
        if mult(i,num) == 1:
            return i
    return -1

print ("Add (74 + 149) = " + str(add(74,149)))
print ("Add (228 + 124) = " + str(add(228,124)))
print ("Subtract (74 - 149) = " + str(subtract(74,149)))
print ("Subtract (228 - 124) = " + str(subtract(228,124)))
print ("Mult (74 * 149) = " + str(mult(74,149)))
print ("Mult (228 * 124) = " + str(mult(228,124)))
print ("Divide (112 / 41) = " + str(div(112,41)))
print ("Divide (69 / 215) = " + str(div(69,215)))

