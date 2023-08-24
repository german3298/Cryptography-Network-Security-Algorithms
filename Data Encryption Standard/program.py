import sys 
import des

#   Program to test my DES algorithm
#   implementation based on strings
#   with the binary representation of
#   keys, plaintexts and ciphertexts.
#
#   @author: Germán Rodríguez


def str_2_bin(text):
    return ''.join(format(i, '08b') for i in bytearray(text, encoding ='utf-8'))

def hex_2_bin(text):
    return bin(int(text, 16))[2:].zfill(64)

def bin_2_str(text):
    bytes_data = int(text, 2).to_bytes((len(text) + 7) // 8, byteorder='big')
    return bytes_data.decode('utf-8')

def bin_2_hex(text):
    return hex(int(text, 2))[2:].upper()

if len(sys.argv) != 3:
    print('Usage: %s <plain_text> <key> ' % sys.argv[0])  
    print('Where: <plain_text> is a string, only 8 chars')
    print('Where: <key> is a string, only 16 hexadecimal chars')
    print('Example: python3 program.py "meetmeat" "9234AB47C3428476"')
    sys.exit(1)

text = sys.argv[1]
binary_plain_text = str_2_bin(text)
key = sys.argv[2]
binary_key = hex_2_bin(key)

print()
print("Plaintext: " + binary_plain_text)
print()

encrypted_binary_text = des.encrypt(binary_plain_text,binary_key)
print("Encrypted binary text: " + encrypted_binary_text)
print("Encrypted text (HEX): " + bin_2_hex(encrypted_binary_text))
print()

decrypted_binary_text = des.decrypt(encrypted_binary_text,binary_key)
print("Decrypted binary text: " + decrypted_binary_text)
print("Decrypted text: " + bin_2_str(decrypted_binary_text))
print()