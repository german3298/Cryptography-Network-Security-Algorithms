import numpy as np
import gmpy
import random
from HillCipher import text_to_numbers_matrix,numbers_matrix_to_text,get_inverse_key, hill_encrypt

# A know plaintext attack can be performed as follows:
# Knowing that we have to obtain a matrix of 
# P’s(plaintext) X, and we can obtain its 
# C(ciphered text) matrix (Y), Y = XK and if X 
# has inverse, X^-1Y = X^-1XK → X^-1Y = IK → K = X^-1Y
# Being K the key matrix that we want to obtain, and
# I the identity matrix
# 
# And for a mxm key matrix, we need m tuples of m numbers
# (0-25, mapped to a-z), which  meet the following 
# requirement:
#   -They must be linearly independent of each other,
#   which is the same that the matrix formed by them
#   must have determinant other than 0 (for the 
#   matrix to have inverse).
#   -The determinant of the matrix mod 26, has to
#   have modulo 26 multiplicative inverse.
#   
#   @author Germán Rodríguez

# Find a mxm matrix key
def find_key(m):
    # First obtain a X matrix that is invertible mod 26
    numbers_matrix = find_inversable_matrix_mxm(m)
    # Normalize to text, to make the plaintext encrypt
    text_to_encrypt = numbers_matrix_to_text(numbers_matrix)
    # Made the ciphertext, and his matrix 
    encrypted_text = encrypt_text(text_to_encrypt,m)
    encrypted_matrix = text_to_numbers_matrix(encrypted_text,m)
    # Obtain the  inverse matrix from the initial X matrix
    inverse_matrix = get_inverse_key(numbers_matrix)
    # Multiply inverse matrix and encrypted matrix, and do mod 26
    key = inverse_matrix @ encrypted_matrix % 26
    return key

#Find randomly an inversable mod 26 matrix mxm
def find_inversable_matrix_mxm (m):
    #Obtain mxm matrix with non-zero determinant
    while True:
        elements = np.random.randint(0,26, (m,m))
        det_mod = round(np.linalg.det(elements) % 26)
        det_inv = int(gmpy.invert(det_mod,26))
        if det_mod != 0 and det_inv != 0:
            break
    return elements

def encrypt_text(text,m):
    encrypted_text = hill_encrypt(text,key_to_analyze,m)
    return encrypted_text

key_to_analyze = np.array(np.mat("12 1 7 8 8;13 10 16 3 25;22 19 20 24 3;0 13 18 20 22;19 18 4 4 1"))
key = find_key(5)
print(key)