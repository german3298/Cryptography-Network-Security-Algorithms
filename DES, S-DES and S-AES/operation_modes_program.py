import sys
import operation_modes as om
import sdes as sd
import des as ds
import saes as sa
from conversions import char_to_strbin, strbin_to_char, strhex_to_strbin, strbin_to_strhex

#   Program to test operation modes
#   with several algorithms of
#   encryption.
#   Inputs like key and plaintext
#   are binary numbers represented
#   as strings.
#
#   @author: Germán Rodríguez

#
#   TESTING CBC IN S-DES ****************************************************************
#

iv = "10101010"
plain_text = "0000000100100011"
key = "0111111101"

sdes = sd.sdes()
cbc = om.cbc()

print()
print("Plaintext: " + plain_text)
print("Key: " + key)
print("Initialization vector: " + iv)
print()

cipher_text = cbc.encrypt(sdes,8,key,iv,plain_text)
print("Cipher text: " + cipher_text)
print()

decrypted_text = cbc.decrypt(sdes,8,key,iv,cipher_text)
print("Decrypted text: " + decrypted_text)
print()

#
#   TESTING CBC IN DES ****************************************************************
#

des = ds.des()
text = "meetmeatholahola"
binary_plain_text = char_to_strbin(text)
key = "9234AB47C3428476"
binary_key = strhex_to_strbin(key)
iv = "0815123B93D2A5C7"
binary_iv = strhex_to_strbin(iv)

print()
print("Binary plaintext: " + binary_plain_text)
print()

cipher_text_binary = cbc.encrypt(des,64,binary_key,binary_iv,binary_plain_text)
print("Cipher text (binary): " + cipher_text_binary)
print("Cipher text (HEX): " + strbin_to_strhex(cipher_text_binary))
print()

decrypted_binary_text = cbc.decrypt(des,64,binary_key,binary_iv,cipher_text_binary)
print("Decrypted text (binary): " + decrypted_binary_text)
print("Decrypted text: " + strbin_to_char(decrypted_binary_text))
print()




