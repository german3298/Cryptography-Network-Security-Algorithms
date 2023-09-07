import math

#   Class to do 4 basic operations in 
#   GF(2⁴) mod x⁴ + x + 1 or
#   GF(2⁸) mod x⁸ + x⁴ + x³ + x + 1 or
#   GF(2^128) mod x^128 + x⁷ + x² + x + 1
#   with coefficients over GF(2)
#   (binary coefficients)
#
#   @author: Germán Rodríguez

class Number_GF:

    IRR_POLY_24= 0b0011 # x⁴ + x + 1
    IRR_POLY_28= 0b00011011 # x⁸ + x⁴ + x³ + x + 1
    IRR_POLY_2128 = 0b10000111 # x^128 + x⁷ + x² + x + 1
    MUL_INV_24=[0,1,9,14,13,11,7,6,15,2,12,5,10,4,3,8]

    def __init__(self, value, order):
        self.value = value
        self.order = order
        self.degree = int(math.log(order,2))
        if self.degree == 4:
            self.irreductible_poly = self.IRR_POLY_24
        elif self.degree == 8:
            self.irreductible_poly = self.IRR_POLY_28
        else:
            self.irreductible_poly = self.IRR_POLY_2128

    def __add__(self, other):
        return Number_GF(self.value ^ other.value, self.order)

    def __sub__(self, other):
        return Number_GF(self.value ^ other.value, self.order)

    def __mul__(self, other):
        """
        We can multiply two elements iterating (i) by the bits of one of 
        them, while we calculate the powers of the other, and when
        the bit is 1, XOR with the i-power
        """
        a = self.value
        b = other.value
        sol = 0
        while b != 0:
            if (b & 1) != 0:
                sol ^= a
            a = self._mul_by_x(a)
            b >>= 1
        return Number_GF(sol, self.order)

    def _mul_by_x(self, num):
        """
        Multiply by x in GF with binary coefficients, it's demostrated 
        to be like a 1 position left shift and, if MSB bit is 1, 
        a XOR with the irreductible poly of the GF.
        If doing the left shift gives a number out of this GF, delete
        that bit with a mask
        """
        msb = num >> (self.degree-1)
        num <<= 1
        mask = (1 << self.degree) - 1
        num &= mask
        if msb == 1:
            num ^= self.irreductible_poly
        return num

    def __truediv__(self, other):
        """
        We have to multiply the mutiplicative inverse of 'other' by 'self'
        """
        return self*other._mul_inv()
            
    def _mul_inv(self):
        """
        We want calculate multiplicative inverse (a^-1):
        a * a^-1 = 1

        Fermat's Little Theorem:
        a^(p^m - 1) = 1
        So,
        a * a^-1 = a^(p^m - 1)
        a^-1 = a^(p^m - 1)/a
        a^-1 = a^(p^m - 1 - 1) divide by a is subtract 1 in exponent
        a^-1 = a^(p^m - 2)
        """
        exp = self.order - 2
        base = Number_GF(self.value,self.order)
        inv = self._fast_exp(base, exp)
        return inv
    
    def _fast_exp(self, base, exp):
        """
        Fast exponentiation recursive algorithm,
        reduces the effort from O(exp) to O(log(exp))
        """
        if exp == 1 : return base
        if exp % 2 == 0:
            res = self._fast_exp(base,exp//2)
            return res * res
        else:
            return self._fast_exp(base,exp-1) * base

    def __str__(self):
        return str(self.value)

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
print()

numD = Number_GF(56742467072460070444459038776914630509,2**128)
numE = Number_GF(324995924687959575801704764228316823997,2**128)

print ("Add (56742467072460070444459038776914630509 + 324995924687959575801704764228316823997) = ")
print(numD+numE) # Answer is 296167389091622931764627063674495719120 in GF(2^128) 
print ("Mult (56742467072460070444459038776914630509 * 324995924687959575801704764228316823997) = ")
print(numD*numE) # Answer is 72927093044932868869406819368353574524 in GF(2^128) 
print ("Divide (56742467072460070444459038776914630509 / 324995924687959575801704764228316823997) = ")
print(numD/numE) # Answer is 213313956644458181727892003155849742090 in GF(2^128)