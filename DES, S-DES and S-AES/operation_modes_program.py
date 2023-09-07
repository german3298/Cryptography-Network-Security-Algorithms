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

mode = om.ctr()

#
#   TESTING MODES IN S-DES ****************************************************************
#

sdes = sd.sdes()
plaintext = "000000010000001000000100"
key = "0111111101"
iv = "00000000"

print()
print("Plaintext: " + plaintext)
print("Key: " + key)
print("Initialization vector (or counter): " + iv)
print()

cipher_text = mode.encrypt(sdes,8,key,iv,plaintext)
print("Cipher text: " + cipher_text)
print()

decrypted_text = mode.decrypt(sdes,8,key,iv,cipher_text)
print("Decrypted text: " + decrypted_text)
print()

#
#   TESTING MODES IN DES ****************************************************************
#

des = ds.des()
text = "meetmeatholahola"
binary_plain_text = char_to_strbin(text)
key = "9234AB47C3428476"
binary_key = strhex_to_strbin(key)
iv = "0815123B93D2A5C8"
binary_iv = strhex_to_strbin(iv)

print()
print("Binary plaintext: " + binary_plain_text)
print()

cipher_text_binary = mode.encrypt(des,64,binary_key,binary_iv,binary_plain_text)
print("Cipher text (binary): " + cipher_text_binary)
print("Cipher text (HEX): " + strbin_to_strhex(cipher_text_binary))
print()

decrypted_binary_text = mode.decrypt(des,64,binary_key,binary_iv,cipher_text_binary)
print("Decrypted text (binary): " + decrypted_binary_text)
print("Decrypted text: " + strbin_to_char(decrypted_binary_text))
print()




