import sys
import saes as sa

#   Program to test my S-AES algorithm
#   implementation based on binary
#   numbers represented as strings.
#
#   @author: Germán Rodríguez

if len(sys.argv) != 3:
    print('Usage: %s <plain_text> <key> ' % sys.argv[0])  
    print('Where: <plain_text> is a string, only 16 bits in binary')
    print('Where: <key> is a string, only 16 bits in binary')
    print('Example: python3 saes_program.py "0110111101101011" "1010011100111011"')
    sys.exit(1)

plain_text = sys.argv[1]
key = sys.argv[2]
saes = sa.saes()

print()
print("Plaintext: " + plain_text)
print()

cipher_text = saes.encrypt(plain_text,key)
print("Cipher text: " + cipher_text)
print()

decrypted_text = saes.decrypt(cipher_text,key)
print("Decrypted text: " + decrypted_text)
print()