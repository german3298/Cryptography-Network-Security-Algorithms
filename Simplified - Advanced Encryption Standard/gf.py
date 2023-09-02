import math

#   Class to do 4 basic operations in 
#   GF(2⁴) mod x⁴ + x + 1 or
#   GF(2⁸) mod x⁸ + x⁴ + x³ + x + 1
#   with coefficients over GF(2)
#
#   @author: Germán Rodríguez

class Number_GF:

    IRR_POLY_24= 0b0011 # x⁴ + x + 1
    IRR_POLY_28= 0b00011011 # x⁸ + x⁴ + x³ + x + 1
    MUL_INV_24=[0,1,9,14,13,11,7,6,15,2,12,5,10,4,3,8]

    def __init__(self, value, order):
        self.value = value
        self.order = order
        self.degree = int(math.log(order,2))
        if self.degree == 4:
            self.irreductible_poly = self.IRR_POLY_24
        else:
            self.irreductible_poly = self.IRR_POLY_28

    def __add__(self, other):
        return self.value ^ other.value

    def __sub__(self, other):
        return self.value ^ other.value

    def __mul__(self, other):
        a = self.value
        b = other.value
        sol = 0
        while b != 0:
            if (b & 1) != 0:
                sol ^= a
            a = self._mul_by_x(a)
            b >>= 1
        return sol

    def _mul_by_x(self, num):
        # Extract MSB bit (degree of GF - 1) to see if it is a 1 or 0 
        msb = num >> (self.degree-1)
        # Left shift to num
        num <<= 1
        # Mask to remove if next bit is 1
        mask = (1 << self.degree) - 1
        num &= mask
        if msb == 1:
            num ^= self.irreductible_poly
        return num

    # Div is multiply by his multiplicative inverse 
    def __truediv__(self, other):
        return self*self._mul_inv(other)

    # Calculate multiplicative inverse on the fly
    def _mul_inv(self, other):
        for i in range(1,other.order):
            gf_n = Number_GF(i,other.order)
            if gf_n*other == 1:
                return gf_n

num1 = Number_GF(1,2**4)
num2 = Number_GF(14,2**4)
num3 = Number_GF(12,2**4)
num4 = Number_GF(5,2**4)

print ("Add (1 + 14) = " + str(num1+num2)) # Answer is 15 in GF(2⁴)
print ("Add (12 + 5) = " + str(num3+num4)) # Answer is 9 in GF(2⁴)
print ("Subtract (1 - 14) = " + str(num1-num2)) # Answer is 15 in GF(2⁴)
print ("Subtract (12 - 5) = " + str(num3-num4)) # Answer is 9 in GF(2⁴)
print ("Mult (1 * 14) = " + str(num1*num2)) # Answer is 14 in GF(2⁴)
print ("Mult (12 * 5) = " + str(num3*num4)) # Answer is 9 in GF(2⁴)
print ("Divide (1 / 14) = " + str(num1/num2)) # Answer is 3 in GF(2⁴)
print ("Divide (12 / 5) = " + str(num3/num4)) # Answer is 13 in GF(2⁴)
print ()

num5 = Number_GF(74,2**8)
num6 = Number_GF(149,2**8)
num7 = Number_GF(228,2**8)
num8 = Number_GF(124,2**8)
num9 = Number_GF(112,2**8)
numA = Number_GF(41,2**8)
numB = Number_GF(69,2**8)
numC = Number_GF(215,2**8)

print ("Add (74 + 149) = " + str(num5+num6)) # Answer is 223 in GF(2⁸)
print ("Add (228 + 124) = " + str(num7+num8)) # Answer is 152 in GF(2⁸)
print ("Subtract (74 - 149) = " + str(num5-num6)) # Answer is 223 in GF(2⁸)
print ("Subtract (228 - 124) = " + str(num7-num8)) # Answer is 152 in GF(2⁸)
print ("Mult (74 * 149) = " + str(num5*num6)) # Answer is 143 in GF(2⁸)
print ("Mult (228 * 124) = " + str(num7*num8)) # Answer is 164 in GF(2⁸) 
print ("Divide (112 / 41) = " + str(num9/numA)) # Answer is 77 in GF(2⁸)
print ("Divide (69 / 215) = " + str(numB/numC)) # Answer is 231 in GF(2⁸)