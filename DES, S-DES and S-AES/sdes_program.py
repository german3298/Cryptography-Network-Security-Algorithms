import sys 
import sdes as sd

#   Program to test my S-DES algorithm
#   implementation based on binary
#   numbers represented as strings.
#
#   @author: Germán Rodríguez

if len(sys.argv) != 3:
    print('Usage: %s <plain_text> <key> ' % sys.argv[0])  
    print('Where: <plain_text> is a string, 8 binary digits')
    print('Where: <key> is a string, 10 binary digits')
    print('Example: python3 sdes_program.py "10010111" "1010000010"')
    sys.exit(1)

plain_text = sys.argv[1]
key = sys.argv[2]
sdes = sd.sdes()
print()
print("Plaintext: " + plain_text)
print()

cipher_text = sdes.encrypt(plain_text,key)
print("Cipher text: " + cipher_text)
print()

decrypted_text = sdes.decrypt(cipher_text,key)
print("Decrypted text: " + decrypted_text)
print()