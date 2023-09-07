import galois
from bit_operations import xor
from conversions import strbin_to_int, int_to_strbin

#   Every needed functions and constants 
#   to encrypt and decrypt with S-AES
#   algorithm.
#   It works with binary numbers in 
#   strings like "00111000" for
#   learning purposes.
#
#   @author: Germán Rodríguez

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

class saes:
    #   Encrypt is only apply the algorithm
    def encrypt(self,text, key, one_round=False):
        generated_keys = generate_keys(key)
        cipher_text = saes_algorithm(text,generated_keys,False, one_round)
        return cipher_text

    #   Decrypt is apply the algorithm with the list of keys reversed
    def decrypt(self,cipher_text,key):
        generated_keys = generate_keys(key)
        generated_keys.reverse()
        text = saes_algorithm(cipher_text,generated_keys,True)
        return text
    
def generate_keys(key):
    keys = []
    keys.append(key)
    w = [""] * 6
    w[0],w[1] = key[0:8], key[8:16]
    ctr = 0
    for i in range(2,6,2):
        w[i] = xor (w[i-2],xor(RCON[ctr],sub_nib(rot_nib(w[i-1]))))
        w[i+1] = xor(w[i],w[i-1])
        left,right = w[i], w[i+1]
        keys.append(left+right)
        ctr += 1
    return keys

def rot_nib(w):
    w_iz, w_der = w[0:4],w[4:8]
    return w_der + w_iz

def sub_nib(w):
    w_iz, w_der = w[0:4],w[4:8]
    w_iz,w_der = s_box_subs(w_iz,False), s_box_subs(w_der,False)
    return w_iz + w_der

def s_box_subs(n, inv):
    ind = strbin_to_int(n)
    if inv == False:
        n_out = S_BOX[ind]
    else:
        n_out = INV_S_BOX[ind]
    n_out = int_to_strbin(n_out, 4)
    return n_out

#   S-AES algorithm applied to a text
def saes_algorithm(text,keys,inv, one_round=False):
    state = xor(text, keys[0])
    state = text_to_matrix(state)
    state = nibble_substitution(state,inv)
    state = shift_rows(state)
    state = mix_columns(state,inv)
    if inv:
        keys[1] = matrix_to_text(mix_columns(text_to_matrix(keys[1]),inv))
    state = xor(matrix_to_text(state), keys[1])
    if one_round:
        return state
    state = text_to_matrix(state)
    state = nibble_substitution(state,inv)
    state = shift_rows(state)
    state = xor(matrix_to_text(state), keys[2])
    return state

def nibble_substitution(matrix,inv):
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            matrix[i][j] = s_box_subs(matrix[i][j],inv)
    return matrix

def shift_rows(matrix):
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
            matrix[i][j] = strbin_to_int(matrix[i][j])
    GF_matrix = GF24(matrix)
    res = constant_matrix @ GF_matrix
    output = res.tolist()
    for j in range(len(output[0])):
        for i in range(len(output)):
            output[i][j] = int_to_strbin(output[i][j],4)
    return output

def text_to_matrix(text):
    matrix = [[text[0:4],text[8:12]],[text[4:8],text[12:16]]]
    return matrix

def matrix_to_text(matrix):
    return matrix[0][0] + matrix[1][0] + matrix[0][1] + matrix[1][1]