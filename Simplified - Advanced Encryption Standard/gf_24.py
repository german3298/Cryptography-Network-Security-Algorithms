#   Calculator to do 4 
#   basic operations in 
#   GF(2⁴) mod x⁴ + x + 1
#   with coefficients over GF(2)
#
#   @author: Germán Rodríguez

IRREDUCTIBLE_POLY= 0b0011 # x⁴ + x + 1
MULTIPLICATIVE_INVERSE=[0,1,9,14,13,11,7,6,15,2,12,5,10,4,3,8]

def add(num1, num2):
    if (not (is_in_gf24(num1))) or (not (is_in_gf24(num2))):
        return -1
    return num1 ^ num2

def subtract(num1, num2):
    if (not (is_in_gf24(num1))) or (not (is_in_gf24(num2))):
        return -1
    return num1 ^ num2

def mult(num1, num2):
    if (not (is_in_gf24(num1))) or (not (is_in_gf24(num2))):
        return -1
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
    for _ in range(3):
        num = mult_by_x(num)
        table.append(num)
    return table

def mult_by_x(num):
    # Extract bit 3 to see if it is a 1 or 0 
    bit_3 = (num >> 3) & 1
    # Left shift to num
    num <<= 1
    # If bit 4 is 1, turn to 0, doing an AND with bit 4 to 0
    num = 0xF & num
    if bit_3 == 1:
        num ^= IRREDUCTIBLE_POLY
    return num

# Div is multiply by his multiplicative inverse 
def div(num1, num2):
    if (not (is_in_gf24(num1))) or (not (is_in_gf24(num2))):
        return -1
    mi = multiplicative_inverse(num2)
    return mult(num1,mi)

def multiplicative_inverse(num):
    return MULTIPLICATIVE_INVERSE[num]

def is_in_gf24(num):
    return num < 16

print ("Add (1 + 14) = " + str(add(1,14)))
print ("Add (12 + 5) = " + str(add(12,5)))
print ("Subtract (1 - 14) = " + str(subtract(1,14)))
print ("Subtract (12 - 5) = " + str(subtract(12,5)))
print ("Mult (1 * 14) = " + str(mult(1,14)))
print ("Mult (12 * 5) = " + str(mult(12,5)))
print ("Divide (1 / 14) = " + str(div(1,14)))
print ("Divide (12 / 5) = " + str(div(12,5)))

