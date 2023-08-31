import sys
import saes

#   One round S-AES attack.
#   
#   @author: Germán Rodríguez

def recover_key(p1,p2,c1,c2):
    alpha = saes.xor(p1,p2)
    print("Alpha: " + alpha)
    alpha = saes.text_to_matrix(alpha)
    beta = saes.xor(c1,c2)
    # Apply inverse mix columns and inverse shift rows
    # to get one-on-one nibble relation with beta
    beta = saes.text_to_matrix(beta)
    beta = saes.mix_columns(beta,True)
    beta = saes.shift_rows(beta)
    str_beta = saes.matrix_to_text(beta)
    print("Beta: " + str_beta)
    # Generate the ddt
    ddt = generate_sbox_ddt()
    # Obtain the possible x's and y's from the ddt 
    probableXYs = [[set(),set()],[set(),set()]]
    for j in range(len(probableXYs[0])):
        for i in range(len(probableXYs)):
            probableXYs[i][j] = ddt[int(alpha[i][j],2)][int(beta[i][j],2)]
    # Do brute-force to test every result obtained since obtaining the key
    matrix_p1 = saes.text_to_matrix(p1)
    for l in probableXYs[1][1]:
        for k in probableXYs[0][1]:
            for j in probableXYs[1][0]:
                for i in probableXYs[0][0]:
                    part_00 = saes.xor(bin(i)[2:].zfill(4),matrix_p1[0][0])
                    part_10 = saes.xor(bin(j)[2:].zfill(4),matrix_p1[1][0])
                    part_01 = saes.xor(bin(k)[2:].zfill(4),matrix_p1[0][1])
                    part_11 = saes.xor(bin(l)[2:].zfill(4),matrix_p1[1][1])
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
            i_str = bin(i)[2:].zfill(4)
            j_str = bin(j)[2:].zfill(4)
            xor = saes.xor(saes.s_box_subs(i_str, False),saes.s_box_subs(j_str, False))
            diff_output = int(xor,2)

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
    print('Example: python3 one_round_attack.py "0110111101101011" "1100001110100101" "1010011100111111"')
    sys.exit(1)

plain_text_1 = sys.argv[1]
plain_text_2 = sys.argv[2]
key = sys.argv[3]

print()
print("Plaintext 1: " + plain_text_1)
print("Plaintext 2: " + plain_text_2)

encrypted_text_1 = saes.encrypt(plain_text_1,key, True)
encrypted_text_2 = saes.encrypt(plain_text_2,key, True)
print("Encrypted plaintext 1: " + encrypted_text_1)
print("Encrypted plaintext 2: " + encrypted_text_2)
print()

recovered_key = recover_key(plain_text_1, plain_text_2, encrypted_text_1, encrypted_text_2)

print("Key: " + key)
print("Recovered Key: " + recovered_key)
print()