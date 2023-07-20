import numpy as np
import sys

def hill_encrypt(text,key):
    pairs_array = text_to_num_arrays(text)
    matrix = np.array(pairs_array)
    pairs_multiply_result = matrix @ key
    pairs_encrypted_numbers = pairs_multiply_result % 26
    encrypted_text = num_arrays_to_text(pairs_encrypted_numbers)
    return encrypted_text

def hill_decrypt(text,key):
    pairs_array = text_to_num_arrays(text)
    matrix = np.array(pairs_array)
    pairs_multiply_result = matrix @ key
    pairs_encrypted_numbers = pairs_multiply_result % 26
    encrypted_text = num_arrays_to_text(pairs_encrypted_numbers)
    return encrypted_text

def text_to_num_arrays (text):
    #Map letters to numbers and insert in an array
    single_array = np.array([ord(char)-ord('a') for char in text])
    #Reshape in several 2 elements arrays 
    pairs_array = single_array.reshape(-1, 2)
    return pairs_array

def num_arrays_to_text (pairs_encrypted_numbers):
    encrypted_numbers = pairs_encrypted_numbers.flatten()
    encrypted_text = "".join([chr(num + 97) for num in encrypted_numbers])
    return encrypted_text

if len(sys.argv) != 3:
    print('Argumentos para ejecutar: %s <text> <key_matrix>' % sys.argv[0])  
    sys.exit(1)
text = sys.argv[1]
key = np.array(np.mat(sys.argv[2]))
encrypted_text = hill_encrypt(text,key)
print("Hill text encrypted: " + hill_encrypt(text,key))
print("Hill text decrypted: " + hill_decrypt(encrypted_text,key))







