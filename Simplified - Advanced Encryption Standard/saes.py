#   Every needed functions and constants 
#   to encrypt and decrypt with S-AES
#   algorithm.
#
#   @author: Germán Rodríguez

import galois

RCON= ["10000000","00110000"]

S_BOX= [9,4,10,11,
        13,1,8,5,
        6,2,0,3,
        12,14,15,7]

INV_S_BOX= [10,5,9,11,
            1,7,8,15,
            6,0,2,3,
            12,4,13,14]

MIX_COL_MATRIX= [[1,4],
                 [4,1]]

INV_MIX_COL_MATRIX= [[9,2],
                     [2,9]]

#   Encrypt is only apply the algorithm
def encrypt(text, key):
    extended_key = extend_key(key)
    cipher_text = saes_algorithm(text,extended_key,False)
    return cipher_text

#   Decrypt is apply the algorithm with the list of keys reversed
def decrypt(cipher_text,key):
    extended_key = extend_key(key)
    extended_key.reverse()
    text = saes_algorithm(cipher_text,extended_key,True)
    return text

#   S-AES algorithm applied to a text
def saes_algorithm(text,keys,inv):
    state = xor(text, keys[0])
    state = text_to_matrix(state)
    state = nibble_substitution(state,inv)
    state = shift_row(state)
    state = mix_columns(state,inv)
    if inv:
        keys[1] = matrix_to_text(mix_columns(text_to_matrix(keys[1]),inv))
    state = text_to_matrix(xor(matrix_to_text(state), keys[1]))
    state = nibble_substitution(state,inv)
    state = shift_row(state)
    state = xor(matrix_to_text(state), keys[2])
    return state

def nibble_substitution(matrix,inv):
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            matrix[i][j] = s_box_subs(matrix[i][j],inv)
    return matrix

def shift_row(matrix):
    matrix[1][0],matrix[1][1] = matrix[1][1],matrix[1][0] 
    return matrix

def mix_columns(matrix,inv):
    GF24 = galois.GF(2**4)
    if inv == False:
        constant_matrix = GF24(MIX_COL_MATRIX)
    else:
        constant_matrix = GF24(INV_MIX_COL_MATRIX)
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            matrix[i][j] = int(matrix[i][j],2)
    GF_matrix = GF24(matrix)
    res = constant_matrix @ GF_matrix
    output = res.tolist()
    for j in range(len(output[0])):
        for i in range(len(output)):
            output[i][j] = bin(output[i][j])[2:].zfill(4)
    return output

def extend_key(key):
    keys = []
    keys.append(key)
    w0,w1 = key[0:8], key[8:16]
    w2 = xor (w0,xor(RCON[0],sub_nib(rot_nib(w1))))
    w3 = xor(w2,w1)
    w4 = xor (w2,xor(RCON[1],sub_nib(rot_nib(w3))))
    w5 = xor(w4,w3)
    keys.append(w2 + w3)
    keys.append(w4 + w5)
    return keys

def rot_nib(w):
    w_iz, w_der = w[0:4],w[4:8]
    return w_der + w_iz

def sub_nib(w):
    w_iz, w_der = w[0:4],w[4:8]
    w_iz,w_der = s_box_subs(w_iz,False), s_box_subs(w_der,False)
    return w_iz + w_der

def s_box_subs(n, inv):
    ind = int(n,2)
    if inv == False:
        n_out = S_BOX[ind]
    else:
        n_out = INV_S_BOX[ind]
    n_out = bin(n_out)[2:].zfill(4)
    return n_out

def xor(input1, input2):
    output = ""
    for n in range(len(input1)):
        if (input1[n] == input2[n]):
            output += "0"
        else:
            output += "1"
    return output

def text_to_matrix(text):
    matrix = [[text[0:4],text[8:12]],[text[4:8],text[12:16]]]
    return matrix

def matrix_to_text(matrix):
    return matrix[0][0] + matrix[1][0] + matrix[0][1] + matrix[1][1]
