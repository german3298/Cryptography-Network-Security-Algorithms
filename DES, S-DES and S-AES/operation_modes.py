from bit_operations import xor,split_same_length

class cbc:
    def encrypt(self, algorithm, block_length, key, iv, plaintext):
        """
        Encryption in cipher block chaining
        :param algorithm: cipher algorithm with encrypt and decrypt methods
        :param block_length: length of the blocks in the cipher algorithm
        :para iv: Initialization vector
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
        :para iv: Initialization vector
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
        