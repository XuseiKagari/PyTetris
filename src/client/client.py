import socket
import struct
from threading import Thread

class Client:

    def __init__(self, addr, figure_storage):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)
        self.__fs = figure_storage

        Thread(target=self.send_new_figure).start()

    def send_new_figure(self):
        figure = self.__fs.get_falling()
        self.sock.sendall(struct.pack('ii6s4s',figure.x, figure.y,  figure.color, figure.get_figure()))

        x, y, color, figure_type = struct.unpack('ii6s4s', self.sock.recv(1024))






