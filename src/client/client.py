import socket
import struct
from threading import Thread

class Client:

    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)

        self.players = []
        Thread(target=self.get_playing_field).start()
