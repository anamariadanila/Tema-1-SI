import socket
import random
import data
from ECB import *
from OFB import *
from AES import *


# possible_modes = [data.ECB, data.OFB]
# operation_mode = random.choice(possible_modes)

print('Possible modes: ')
print('1. ECB')
print('2. OFB')
option = input("Choose mode: ")
if option == '1':
    operation_mode = data.ECB
if option == '2':
    operation_mode = data.OFB

key = b''

key_encrypted = b''


def message_encrypt(message):  # se cripteaza mesajul cu modul ales
    if operation_mode == data.ECB:
        ecb = ECB(data.vector_initialization, key)
        message_encrypted = ecb.encrypt(message)
    else:
        ofb = OFB(data.vector_initialization, key)
        message_encrypted = ofb.encrypt(message)
    return message_encrypted


def read_from_file(file):  # se citeste textul din fisier
    try:
        file = file.read()
        return file
    except PermissionError:
        print("Can not access the file")


def connection_KM(KM_port):  # se realizeaza conexiunea cu KM
    global key, key_encrypted
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as kms:
        kms.connect((data.HOST, KM_port))

        # se trimite modul de operare ales
        kms.sendall(bytes(operation_mode, "utf-8"))
        kms.sendall(key_encrypted)

        # se primeste si se decripteaza cheia
        key_encrypted = kms.recv(16)
        print(f'The key has been received from KM node: {key_encrypted}')
        key = aes_decrypt(key_encrypted, data.K_prim)
        print(f'Decrypted key: {key}')


def connection_B(B_port):  # se realizeaza conexiunea cu B
    global key, key_encrypted
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((data.HOST, B_port))

        # se trimite modul de operare ales
        s.sendall(bytes(operation_mode, "utf-8"))
        s.sendall(key_encrypted)

        # se primeste semnalul de start
        info = s.recv(5)
        print(f'B sent the signal: {info.decode("utf-8")}')

        try:

            with open("file.txt", "rb") as f:
                file = read_from_file(f)

                # se trimite dimensiunea textului citit din fisier
                size = len(file)
                s.sendall(bytes(str(size), 'utf8'))

                message_encrypted = message_encrypt(file)

                # se trimite mesajul criptat
                print(f'The encrypted message has been sent: {message_encrypted} ')
                s.sendall(message_encrypted)

        except FileNotFoundError:
            print("Did not find the requested file")


if __name__ == "__main__":
    connection_KM(data.KM_PORT)
    connection_B(data.B_PORT)
