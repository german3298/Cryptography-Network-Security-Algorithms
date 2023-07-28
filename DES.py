INITIAL_PERMUTATION=   [58, 50, 42, 34, 26, 18, 10, 2,
                        60, 52, 44, 36, 28, 20, 12, 4,
                        62, 54, 46, 38, 30, 22, 14, 6,
                        64, 56, 48, 40, 32, 24, 16, 8,
                        57, 49, 41, 33, 25, 17, 9, 1,
                        59, 51, 43, 35, 27, 19, 11, 3,
                        61, 53, 45, 37, 29, 21, 13, 5,
                        63, 55, 47, 39, 31, 23, 15, 7]

INVERSE_INITIAL_PERMUTATION=   [40, 8, 48, 16, 56, 24, 64, 32,
                                39, 7, 47, 15, 55, 23, 63, 31,
                                38, 6, 46, 14, 54, 22, 62, 30,
                                37, 5, 45, 13, 53, 21, 61, 29,
                                36, 4, 44, 12, 52, 20, 60, 28,
                                35, 3, 43, 11, 51, 19, 59, 27,
                                34, 2, 42, 10, 50, 18, 58, 26,
                                33, 1, 41, 9, 49, 17, 57, 25]

EXPANSION_PERMUTATION= [32, 1, 2, 3, 4, 5, 4, 5,
                        6, 7, 8, 9, 8, 9, 10, 11,
                        12, 13, 12, 13, 14, 15, 16, 17,
                        16, 17, 18, 19, 20, 21, 20, 21,
                        22, 23, 24, 25, 24, 25, 26, 27,
                        28, 29, 28, 29, 30, 31, 32, 1]

PERMUTATION_FUNCTION=  [16,  7, 20, 21,
                        29, 12, 28, 17,
                        1, 15, 23, 26,
                        5, 18, 31, 10,
                        2,  8, 24, 14,
                        32, 27,  3,  9,
                        19, 13, 30,  6,
                        22, 11,  4, 25]

PERMUTED_CHOICE_ONE=   [57, 49, 41, 33, 25, 17, 9,
                        1, 58, 50, 42, 34, 26, 18,
                        10, 2, 59, 51, 43, 35, 27,
                        19, 11, 3, 60, 52, 44, 36,
                        63, 55, 47, 39, 31, 23, 15,
                        7, 62, 54, 46, 38, 30, 22,
                        14, 6, 61, 53, 45, 37, 29,
                        21, 13, 5, 28, 20, 12, 4]

PERMUTED_CHOICE_TWO=   [14, 17, 11, 24, 1, 5,
                        3, 28, 15, 6, 21, 10,
                        23, 19, 12, 4, 26, 8,
                        16, 7, 27, 20, 13, 2,
                        41, 52, 31, 37, 47, 55,
                        30, 40, 51, 45, 33, 48,
                        44, 49, 39, 56, 34, 53,
                        46, 42, 50, 36, 29, 32]

KEY_SCHEDULE= [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]

def encrypt(text, keys):
    cipher_text = permute(text, INITIAL_PERMUTATION)
    left,right = cipher_text[0:32], cipher_text[32:]
    left,right = feistel_cipher(left,right,keys,0)
    cipher_text = left + right
    cipher_text = permute(cipher_text, INVERSE_INITIAL_PERMUTATION)
    return cipher_text

def decrypt(cipher_text,keys):
    text = permute(cipher_text, INITIAL_PERMUTATION)
    left,right = text[0:32], text[32:]
    keys = keys.reverse()
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
        left,right = permute(C,PERMUTED_CHOICE_TWO),permute(D,PERMUTED_CHOICE_TWO)
        keys = keys.append(left + right)
    return keys

def left_shift(input,shifts):
    while (shifts > 0):
        input = input[1:].append(input[0:1])
        shifts -= 1
    return input

def permute(input,new_positions):
    output = ""
    for n in range(len(new_positions)):
        output[n]=input[new_positions[n]-1]
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

def s_boxes(input,key):
    groups6 = [input[i:i+8] for i in range(0, input, 8)]
    output = ""
    for i in range(len(groups6)):
        s_box(i, groups6[i])
    return output

####WIP######
def s_box(index, text):
    output = permute 
    return output

def xor(input1, input2):
    output = ""
    for n in range(len(input1)):
        if (input1[n] == input2[n]):
            output += "0"
        else:
            output += "1"
    return output