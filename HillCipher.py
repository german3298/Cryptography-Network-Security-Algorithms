import numpy as np
import sys
import gmpy

#Hill encryption given a text multiple of 2 and a matrix key (with multiplicative inverse)
def hill_encrypt(text,key):
    pairs_array = text_to_num_arrays(text)
    matrix = np.array(pairs_array)
    pairs_multiply_result = matrix @ key
    pairs_encrypted_numbers = pairs_multiply_result % 26
    encrypted_text = num_arrays_to_text(pairs_encrypted_numbers)
    return encrypted_text

#Hill decryption given a text multiple of 2 and a matrix key (with multiplicative inverse)
def hill_decrypt(text,key):
    pairs_array = text_to_num_arrays(text)
    matrix = np.array(pairs_array)
    inverse_key = get_inverse_key(key)
    pairs_multiply_result = matrix @ inverse_key
    pairs_decrypted_numbers = pairs_multiply_result % 26
    decrypted_text = num_arrays_to_text(pairs_decrypted_numbers)
    return decrypted_text

def text_to_num_arrays (text):
    #Map letters to numbers and insert in an array
    single_array = np.array([ord(char)-ord('a') for char in text])
    #Reshape in several 2 elements arrays 
    pairs_array = single_array.reshape(-1, 2)
    return pairs_array

def num_arrays_to_text (pairs_numbers):
    numbers = pairs_numbers.flatten()
    text = "".join([chr(num + 97) for num in numbers])
    return text

def get_inverse_key (key):
    inv_key = np.array(key,copy=True)
    #Det of the matrix mod 26
    det_mod = round(np.linalg.det(key) % 26)
    #Modular multiplicative inverse mod 26 from the det
    det_inverse = int(gmpy.invert(det_mod,26))
    #Change element 11 for element 22 in the key matrix
    inv_key[0, 0],inv_key[1,1] = inv_key[1,1],inv_key[0,0]
    #Add the negative to the other elements
    inv_key[0, 1],inv_key[1, 0] = -inv_key[0, 1],-inv_key[1, 0]
    #Multiply the matrix by the inverse of the det and do the mod 26
    inv_key = det_inverse*inv_key % 26
    return inv_key

if len(sys.argv) != 3:
    print('Usage: %s <text> <key_matrix>' % sys.argv[0])  
    print('Use only multiples of 2 in the text, and only allowed matrices as keys')
    print ('Example: python3 HillCipher.py "meetmeate" "5 8;17 3"')
    sys.exit(1)
text = sys.argv[1]
key = np.array(np.mat(sys.argv[2]))
encrypted_text = hill_encrypt(text,key)
print("Hill text encrypted: " + hill_encrypt(text,key))
print("Hill text decrypted: " + hill_decrypt(encrypted_text,key))







