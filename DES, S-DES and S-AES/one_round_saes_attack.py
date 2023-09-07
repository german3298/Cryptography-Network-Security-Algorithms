import sys
import saes as sa
from bit_operations import xor
from conversions import int_to_strbin, strbin_to_int


#   One round S-AES differential attack.
#   
#   @author: Germán Rodríguez

def recover_key(p1,p2,c1,c2):
    alpha = xor(p1,p2)
    # print("Alpha: " + alpha)
    alpha = sa.text_to_matrix(alpha)
    beta = xor(c1,c2)
    # Apply inverse mix columns and inverse shift rows
    # to get one-on-one nibble relation with beta
    beta = sa.text_to_matrix(beta)
    beta = sa.mix_columns(beta,True)
    beta = sa.shift_rows(beta)
    #str_beta = sa.matrix_to_text(beta)
    #print("Beta: " + str_beta)
    # Generate the ddt
    ddt = generate_sbox_ddt()
    # Obtain the possible x's and y's from the ddt 
    probableXYs = [[set(),set()],[set(),set()]]
    for j in range(len(probableXYs[0])):
        for i in range(len(probableXYs)):
            probableXYs[i][j] = ddt[strbin_to_int(alpha[i][j])][strbin_to_int(beta[i][j])]
    # Do brute-force to test every result obtained since obtaining the key
    saes = sa.saes()
    matrix_p1 = sa.text_to_matrix(p1)
    for l in probableXYs[1][1]:
        for k in probableXYs[0][1]:
            for j in probableXYs[1][0]:
                for i in probableXYs[0][0]:
                    part_00 = xor(int_to_strbin(i,4),matrix_p1[0][0])
                    part_10 = xor(int_to_strbin(j,4),matrix_p1[1][0])
                    part_01 = xor(int_to_strbin(k,4),matrix_p1[0][1])
                    part_11 = xor(int_to_strbin(l,4),matrix_p1[1][1])
                    new_key = part_00 + part_10 + part_01 + part_11
                    # if we encrypt p1 and obtain c1, is the correct key
                    encrypted_text = saes.encrypt(p1,new_key,True)
                    if c1 == encrypted_text:
                        return new_key
    return "Key not founded"

# Code to generate the sbox Differential Distribution Table
def generate_sbox_ddt():
    """
        this function is an adaptation of
        code from Merricx
        https://github.com/merricx
    """
    table = [[]] * 16
    for i in range(16):
        for j in range(16):
            diff_input = i ^ j
            i_str = int_to_strbin(i,4)
            j_str = int_to_strbin(j,4)
            xor_res = xor(sa.s_box_subs(i_str, False),sa.s_box_subs(j_str, False))
            diff_output = int(xor_res,2)

            if len(table[diff_input]) != 0:
                table[diff_input][diff_output].update(set([i, j]))
            else:
                table[diff_input] = [set() for _ in range(16)]
                table[diff_input][diff_output] = set([i, j])
    return table

if len(sys.argv) != 4:
    print('Usage: %s <plain_text_1> <plain_text_2> <key> ' % sys.argv[0])  
    print('Where: <plain_text_?> are strings, only 16 bits in binary')
    print('Where: <key> is a string, only 16 bits in binary')
    print('Example: python3 one_round_saes_attack.py "0110111101101011" "1100001110100101" "1010011100111111"')
    sys.exit(1)

plain_text_1 = sys.argv[1]
plain_text_2 = sys.argv[2]
key = sys.argv[3]

print()
print("Plaintext 1: " + plain_text_1)
print("Plaintext 2: " + plain_text_2)

saes = sa.saes()
cipher_text_1 = saes.encrypt(plain_text_1,key, True)
cipher_text_2 = saes.encrypt(plain_text_2,key, True)
print("Cipher text 1: " + cipher_text_1)
print("Cipher text 2: " + cipher_text_2)
print()

recovered_key = recover_key(plain_text_1, plain_text_2, cipher_text_1, cipher_text_2)

print("Key: " + key)
print("Recovered Key: " + recovered_key)
print()