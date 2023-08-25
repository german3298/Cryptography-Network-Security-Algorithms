import sys
import saes

#   Program to test my S-AES algorithm
#   implementation based on strings
#   with the binary representation of
#   keys, plaintexts and ciphertexts.
#
#   @author: Germán Rodríguez

if len(sys.argv) != 3:
    print('Usage: %s <plain_text_binary> <key_binary> ' % sys.argv[0])  
    print('Where: <plain_text_binary> is a string, only 16 bits in binary')
    print('Where: <key_binary> is a string, only 16 bits in binary')
    print('Example: python3 program.py "0110111101101011" "1010011100111011"')
    sys.exit(1)

binary_plain_text = sys.argv[1]
binary_key = sys.argv[2]

print()
print("Plaintext: " + binary_plain_text)
print()

encrypted_binary_text = saes.encrypt(binary_plain_text,binary_key)
print("Encrypted binary text: " + encrypted_binary_text)
print()

decrypted_binary_text = saes.decrypt(encrypted_binary_text,binary_key)
print("Decrypted binary text: " + decrypted_binary_text)
print()