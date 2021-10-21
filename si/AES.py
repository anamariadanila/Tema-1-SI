from Crypto.Cipher import AES


def aes_encrypt(message, key):
    aes = AES.new(key, AES.MODE_ECB)
    encrypted = aes.encrypt(message)
    return encrypted


def aes_decrypt(ciphertext, key):
    aes = AES.new(key, AES.MODE_ECB)
    decrypted = aes.decrypt(ciphertext)
    return decrypted
