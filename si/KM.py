import os
import socket
from AES import *
from data import *

K = os.urandom(16)  # pentru a genera cheia K random

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, KM_PORT))
    s.listen()
    conn, _ = s.accept()
    with conn:
        data = conn.recv(3)
        print(f'Operation mode requested: {data.decode("utf-8")}')
        conn.sendall(bytes(aes_encrypt(K, K_prim)))
