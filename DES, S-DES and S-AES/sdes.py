from bit_operations import *
from conversions import strbin_to_int, int_to_strbin

#   Every needed functions and constants 
#   to encrypt and decrypt with S-DES 
#   algorithm. 
#   It works with binary numbers in 
#   strings like "00111000" for
#   learning purposes.
#   
#   @author: Germán Rodríguez

INITIAL_PERMUTATION=   [2,6,3,1,
                        4,8,5,7]

INVERSE_INITIAL_PERMUTATION=   [4,1,3,5,
                                7,2,8,6]

EXPANSION_PERMUTATION= [4,1,2,3,
                        2,3,4,1]

PERMUTATION_FUNCTION=  [2,4,3,1]

S_BOXES = [[[1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 3, 2]],

           [[0, 1, 2, 3],
            [2, 0, 1, 3],
            [3, 0, 1, 0],
            [2, 1, 0, 3]]]

P10=[3,5,2,7,4, 
    10,1,9,8,6]

P8=[6,3,7,4,
    8,5,10,9]

KEY_SCHEDULE= [1, 2]

class sdes:
    #   Encrypt is only apply the algorithm
    def encrypt(self, text, key):
        generated_keys = generate_keys(key)
        cipher_text = sdes_algorithm(text,generated_keys)
        return cipher_text

    #   Decrypt is apply the algorithm with the list of keys reversed
    def decrypt(self, cipher_text,key):
        generated_keys = generate_keys(key)
        generated_keys.reverse()
        text = sdes_algorithm(cipher_text,generated_keys)
        return text

def generate_keys(key):
    keys = []
    key10 = permute(key,P10)
    C,D = key10[0:5], key10[5:]
    for n in KEY_SCHEDULE:
        C,D = left_shift(C,n),left_shift(D,n)
        k = permute(C+D,P8)
        keys.append(k)
    return keys

def sdes_algorithm(text,keys):
    text = permute(text, INITIAL_PERMUTATION)
    left,right = text[0:4], text[4:]
    left,right = feistel_cipher(left,right,keys,0)
    text = left + right
    text = permute(text, INVERSE_INITIAL_PERMUTATION)
    return text

def feistel_cipher(left,right,keys,rounds):
    if (rounds == 2):
        return right,left
    left,right = right, xor(left,f_function (right, keys[rounds]))
    return feistel_cipher(left,right,keys,rounds+1)

def permute(input,new_positions):
    output = ""
    for n in range(len(new_positions)):
        output+=input[new_positions[n]-1]
    return output

def f_function(input,key):
    output = permute(input,EXPANSION_PERMUTATION)
    output = xor(key,output)
    output = s_boxes(output)
    output = permute(output,PERMUTATION_FUNCTION)
    return output

def s_boxes(input):
    groups4 = split_same_length(input,4)
    output = ""
    for i in range(len(groups4)):
        output += s_box(i, groups4[i]) 
    return output

def s_box(index, text):
    #Divide first and last bits to select row
    row = strbin_to_int(text[0]+text[-1])
    #The middle bits to select column
    col = strbin_to_int(text[1:-1])
    output_num = S_BOXES[index][row][col]
    output = int_to_strbin(output_num,2)
    return output