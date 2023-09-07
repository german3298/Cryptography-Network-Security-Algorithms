from bit_operations import xor,split_same_length
from conversions import strbin_to_int, int_to_strbin

class cbc:
    """
    Cipher block chaining mode
    """
    def encrypt(self, algorithm, block_length, key, iv, plaintext):
        """
        Encryption in cipher block chaining
        :param algorithm: cipher algorithm with encrypt and decrypt methods
        :param block_length: length of the blocks in the cipher algorithm
        :param iv: Initialization vector
        """
        cipher_texts = ""
        plaintext_blocks = split_same_length(plaintext,block_length)
        c = iv
        for b in plaintext_blocks:
            input = xor(c, b)
            c = algorithm.encrypt(input,key)
            cipher_texts += c
        return cipher_texts
    
    def decrypt(self, algorithm, block_length, key, iv, ciphertext):
        """
        Decryption in cipher block chaining
        :param algorithm: cipher algorithm with encrypt and decrypt methods
        :param block_length: length of the blocks in the cipher algorithm
        :param iv: Initialization vector
        """
        plain_texts = ""
        ciphertext_blocks = split_same_length(ciphertext,block_length)
        last_b = iv
        for b in ciphertext_blocks:
            output = algorithm.decrypt(b,key)
            p = xor(output, last_b)
            last_b = b
            plain_texts += p
        return plain_texts

class cfb:
    """
    Cipher feedback mode
    """
    def encrypt(self, algorithm, unit_length, key, iv, plaintext):
        """
        Encryption in cipher feedback
        :param algorithm: cipher algorithm with encrypt and decrypt methods
        :param unit_length: length of the units of transmission
        :param iv: Initialization vector
        """
        cipher_texts = ""
        plaintext_units = split_same_length(plaintext,unit_length)
        i = iv
        for b in plaintext_units:
            output = algorithm.encrypt(i,key)
            c = xor(b,output[0:unit_length])
            cipher_texts += c
            i = i[unit_length:] + c
        return cipher_texts
    
    def decrypt(self, algorithm, unit_length, key, iv, ciphertext):
        """
        Decryption in cipher feedback
        :param algorithm: cipher algorithm with encrypt and decrypt methods
        :param unit_length: length of the units of transmission
        :param iv: Initialization vector
        """
        plaintexts = ""
        ciphertext_units = split_same_length(ciphertext,unit_length)
        i = iv
        for b in ciphertext_units:
            output = algorithm.encrypt(i,key)
            p = xor(b,output[0:unit_length])
            plaintexts += p
            i = i[unit_length:] + b
        return plaintexts
    
class ctr:
    """
    Cipher in counter mode
    """
    def encrypt(self, algorithm, block_length, key, ctr, plaintext):
        """
        Encryption in counter mode
        :param algorithm: cipher algorithm with encrypt and decrypt methods
        :param block_length: length of the blocks in the cipher algorithm
        :param ctr: Starting number of the counter
        """
        cipher_texts = ""
        plaintext_blocks = split_same_length(plaintext,block_length)
        c = ctr
        for b in plaintext_blocks:
            output = algorithm.encrypt(c,key)
            cipher_texts += xor(output, b)
            int_c = strbin_to_int(c) + 1
            c = int_to_strbin(int_c, len(ctr))
        return cipher_texts
    
    def decrypt(self, algorithm, block_length, key, ctr, ciphertext):
        return self.encrypt(algorithm,block_length,key,ctr,ciphertext)
        