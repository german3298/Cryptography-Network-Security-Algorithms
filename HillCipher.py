import numpy as np
import gmpy

#
#   @author Germán Rodríguez
#

# Hill encryption given a text multiple of m and a matrix key (with multiplicative inverse)
def hill_encrypt(text,key,m):
    encrypted_text = make_substitution(text,key,m)
    return encrypted_text

# Hill decryption given a text multiple of m and a matrix key (with multiplicative inverse)
def hill_decrypt(text,key,m):
    inverse_key = get_inverse_key(key)
    decrypted_text = make_substitution(text,inverse_key,m)
    return decrypted_text

# Makes the hill multiplication and obtains the text
def make_substitution (text, key_matrix,m):
    m_array = text_to_numbers_matrix(text,m)
    #Multiply every m array by the key matrix, and add % 26
    m_multiply_result = m_array @ key_matrix % 26
    text = numbers_matrix_to_text(m_multiply_result)
    return text

def text_to_numbers_matrix(text,m):
    #Map letters to numbers and insert in an array
    single_array = np.array([ord(char)-ord('a') for char in text])
    #Reshape in several m elements arrays 
    m_array = single_array.reshape(-1, m)
    return m_array

def numbers_matrix_to_text(numbers_matrix):
    #Flatten to convert a single array
    numbers = numbers_matrix.flatten()
    #Map numbers to letters and join them in a string
    text = "".join([chr(num + 97) for num in numbers])
    return text

# Get inverse for key_matrix mod 26
def get_inverse_key (key):
    inv_key = np.array(key,copy=True)
    #Det of the matrix mod 26
    det_mod = round(np.linalg.det(key) % 26)
    #Modular multiplicative inverse mod 26 from the det
    det_inverse = int(gmpy.invert(det_mod,26))
    #Obtain the adjoint matrix
    adjoint_key = adjoint_matrix(key)
    #Multiply the adjoint matrix by the inverse of the det and do the mod 26
    inv_key = det_inverse*adjoint_key % 26
    return inv_key

# The adjoint of a matrix (inefficient, have to change for loops)
def adjoint_matrix (matrix):
    rows, cols = matrix.shape
    adjoint_matrix = np.zeros_like(matrix)
    for i in range(rows):
        for j in range(cols):
            submat = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            cofactor = (-1) ** (i + j) * round(np.linalg.det(submat))
            adjoint_matrix[j, i] = cofactor
    return adjoint_matrix

