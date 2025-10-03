import socket
import struct
from threading import Thread
from figure import Figure

HOST, PORT = 'localhost', 65432
MAX_PLAYERS = 2

class Server:
    def __init__(self, addr, max_coon):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(addr)
        self.__figures = []

        self.s.listen()
        self.listen()

    def listen(self):
        while True:
            if 1 < 2:
                conn, addr = self.s.accept()

                print("New connection", addr)

                Thread(target=self.handle_client,
                       args=(conn,)).start()

    def handle_client(self, conn):

        while True:
            try:
                data = conn.recv(1024)

                if not data:
                    break

                x, y, color, fig_type = struct.unpack('bbbb', data)
                print("x:%(x)s, y:%(y)s, color:%(color)s, type:%(type)s" % {"x": x, "y": y, "color": color, "type": fig_type})
                conn.sendall(data)

            except Exception as e:
                print(e)
                break


if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)




