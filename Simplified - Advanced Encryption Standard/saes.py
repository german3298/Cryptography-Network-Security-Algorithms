#   Every needed functions and constants 
#   to encrypt and decrypt with S-AES 
#   algorithm.
#   
#   @author: Germán Rodríguez

EXPANSION_PERMUTATION= [32, 1, 2, 3, 4, 5, 4, 5,
                        6, 7, 8, 9, 8, 9, 10, 11,
                        12, 13, 12, 13, 14, 15, 16, 17,
                        16, 17, 18, 19, 20, 21, 20, 21,
                        22, 23, 24, 25, 24, 25, 26, 27,
                        28, 29, 28, 29, 30, 31, 32, 1]


#   Encrypt is only apply the algorithm
def encrypt(text, keys):
    cipher_text = DES_algorithm(text,keys)
    return cipher_text

#   Decrypt is apply the algorithm with the list of keys reversed
def decrypt(cipher_text,keys):
    keys.reverse()
    text = DES_algorithm(cipher_text,keys)
    return text

#   DES algorithm applied to a text
def DES_algorithm(text,keys):
    text = permute(text, INITIAL_PERMUTATION)
    left,right = text[0:32], text[32:]
    left,right = feistel_cipher(left,right,keys,0)
    text = left + right
    text = permute(text, INVERSE_INITIAL_PERMUTATION)
    return text

def prepare_keys(key):
    keys = []
    key56 = permute(key,PERMUTED_CHOICE_ONE)
    C,D = key56[0:28], key56[28:56]
    for n in KEY_SCHEDULE:
        C,D = left_shift(C,n),left_shift(D,n)
        k = permute(C+D,PERMUTED_CHOICE_TWO)
        keys.append(k)
    return keys

def left_shift(input,shifts):
    while (shifts > 0):
        input = input[1:]+input[0:1]
        shifts -= 1
    return input

def permute(input,new_positions):
    output = ""
    for n in range(len(new_positions)):
        output+=input[new_positions[n]-1]
    return output

def feistel_cipher(left,right,keys,rounds):
    if (rounds == 16):
        return right,left
    left,right = right, xor(left,f_function (right, keys[rounds]))
    return feistel_cipher(left,right,keys,rounds+1)

def f_function(input,key):
    output = permute(input,EXPANSION_PERMUTATION)
    output = xor(key,output)
    output = s_boxes(output)
    output = permute(output,PERMUTATION_FUNCTION)
    return output

def s_boxes(input):
    #Divide in groups of 6 bits
    groups6 = [input[i:i+6] for i in range(0, len(input), 6)]
    output = ""
    for i in range(len(groups6)):
        output += s_box(i, groups6[i]) 
    return output

def s_box(index, text):
    #Divide first and last bits to select row
    row = int(text[0]+text[-1],2)
    #The middle bits to select column
    col = int(text[1:-1],2)
    output = S_BOXES[index][row][col]
    #Transform int into his string binary representation
    output = bin(output)[2:].zfill(4)
    return output

def xor(input1, input2):
    output = ""
    for n in range(len(input1)):
        if (input1[n] == input2[n]):
            output += "0"
        else:
            output += "1"
    return output