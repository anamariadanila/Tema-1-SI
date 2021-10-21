import socket
import data
from ECB import *
from OFB import *
from AES import *

key = b''

key_encrypted = b''


def get_operation_mode():  # se primeste modul de operare
    mode = conn.recv(3)
    print(f'Operation mode: {mode.decode("utf-8")}')
    return mode


def get_message():
    size = conn.recv(4)
    return conn.recv(int(str(size, 'utf8')))


def message_decrypt(mode, message):  # se decripteaza mesajul cu modul ales
    if mode == data.ECB:
        ecb = ECB(data.vector_initialization, key)
        message_decrypted = ecb.decrypt(message)
    else:
        ofb = OFB(data.vector_initialization, key)
        message_decrypted = ofb.decrypt(message)
    return message_decrypted


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((data.HOST, data.B_PORT))
    s.listen()
    conn, _ = s.accept()
    with conn:
        mode_of_operation = get_operation_mode()

        # se primeste cheia si se decripteaza
        key_encrypted = conn.recv(16)
        print(f'Key from A: {key_encrypted}')
        key = aes_decrypt(key_encrypted, data.K_prim)
        print(f'Decrypted key: {key}')

        # se trimite semnalul de start
        conn.sendall(bytes("Start", "utf-8"))

        decrypted_message = message_decrypt(mode_of_operation.decode('utf-8'), get_message())

        print(f'Message from A: {decrypted_message.decode("ISO-8859-1")}')
