import sys 
import des as ds
from conversions import char_to_strbin, strbin_to_char, strhex_to_strbin, strbin_to_strhex

#   Program to test my DES algorithm
#   implementation based on binary
#   numbers represented as strings.
#   
#   @author: Germán Rodríguez

if len(sys.argv) != 3:
    print('Usage: %s <plain_text> <key> ' % sys.argv[0])  
    print('Where: <plain_text> is a string, 8 ASCII chars')
    print('Where: <key> is a string, 16 hexadecimal chars')
    print('Example: python3 des_program.py "meetmeat" "9234AB47C3428476"')
    sys.exit(1)

des = ds.des()
text = sys.argv[1]
binary_plain_text = char_to_strbin(text)
key = sys.argv[2]
binary_key = strhex_to_strbin(key)

print()
print("Binary plaintext: " + binary_plain_text)
print()

cipher_text_binary = des.encrypt(binary_plain_text,binary_key)
print("Cipher text (binary): " + cipher_text_binary)
print("Cipher text (HEX): " + strbin_to_strhex(cipher_text_binary))
print()

decrypted_binary_text = des.decrypt(cipher_text_binary,binary_key)
print("Decrypted text (binary): " + decrypted_binary_text)
print("Decrypted text: " + strbin_to_char(decrypted_binary_text))
print()