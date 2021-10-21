class OFB:
    def __init__(self, init_vector, key):
        self.vector_initialization = init_vector
        self.key = key

    def encrypt(self, plaintext):
        ciphertext = b''
        init_vector = self.vector_initialization
        while plaintext:
            block = plaintext[0:16]
            block = block + b'\0' * (16 - len(block)) #daca este necesar se va face padding
            plaintext = plaintext[16:]
            encrypted_block = function_xor(init_vector, block, self.key)
            ciphertext += encrypted_block
            init_vector = bytes(a ^ b for (a, b) in zip(self.key, init_vector))
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b''
        init_vector = self.vector_initialization
        while ciphertext:
            block = ciphertext[0:16]
            ciphertext = ciphertext[16:]
            decrypted_block = function_xor(init_vector, self.key, block)
            plaintext += decrypted_block
            init_vector = bytes(a ^ b for (a, b) in zip(self.key, init_vector))
        return plaintext


def function_xor(block, init_vector, key):
    block_xor_init_vector = bytes(a ^ b for (a, b) in zip(block, init_vector))
    block_xor_init_vector_xor_key = bytes(a ^ b for (a, b) in zip(block_xor_init_vector, key))
    return block_xor_init_vector_xor_key
