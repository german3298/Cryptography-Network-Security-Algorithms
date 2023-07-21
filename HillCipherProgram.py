import numpy as np
import sys
import HillCipher as hc

if len(sys.argv) != 4:
    print('Usage: %s <text> <key_matrix> <dimensions>' % sys.argv[0])  
    print('Use only text with nº of chars multiple of <dimensions>')
    print('Use only allowed matrices (with multiplicative inverse mod 26)')
    print('Example: python3 HillCipher.py "meetmeate" "5 8;17 3" "2"')
    sys.exit(1)
text = sys.argv[1]
key = np.array(np.mat(sys.argv[2]))
dimension = int(sys.argv[3])
encrypted_text = hc.hill_encrypt(text,key,dimension)
print("Hill text encrypted: " + encrypted_text)
print("Hill text decrypted: " + hc.hill_decrypt(encrypted_text,key,dimension))