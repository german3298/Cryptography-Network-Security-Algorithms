import sys
import saes

#   Program to test my S-AES algorithm
#   implementation based on strings
#   with the binary representation of
#   keys, plaintexts and ciphertexts.
#
#   @author: Germán Rodríguez

if len(sys.argv) != 3:
    print('Usage: %s <plain_text> <key> ' % sys.argv[0])  
    print('Where: <plain_text> is a string, only 16 bits in binary')
    print('Where: <key> is a string, only 16 bits in binary')
    print('Example: python3 program.py "0110111101101011" "1010011100111011"')
    sys.exit(1)

plain_text = sys.argv[1]
key = sys.argv[2]

print()
print("Plaintext: " + plain_text)
print()

encrypted_text = saes.encrypt(plain_text,key)
print("Encrypted text: " + encrypted_text)
print()

decrypted_text = saes.decrypt(encrypted_text,key)
print("Decrypted text: " + decrypted_text)
print()