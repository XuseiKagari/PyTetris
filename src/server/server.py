import socket
import struct
from threading import Thread
from figure_s import FigureServer
from figure_storage_s import FigureStorageServer

HOST, PORT = 'localhost', 65432
MAX_PLAYERS = 2


class Server:
    def __init__(self, addr, max_coon):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(addr)
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
        fs = FigureStorageServer
        while True:
            try:
                com = conn.recv(1)

                if not com:
                    break
                com = struct.unpack('c', com)[0]

                if com == b'N':
                    data = conn.recv(5)
                    ids, x, y, color, fig_type = struct.unpack('bbbbb', data)
                    fig = FigureServer(ids, x, y, color, fig_type)
                    fs.set_falling(fig)
                    print("id%(id)s, x:%(x)s, y:%(y)s, color:%(color)s, type:%(type)s" % {"id": ids, "x": x, "y": y,
                                                                                          "color": color,
                                                                                          "type": fig_type})

                if com == b'D':
                    data = conn.recv(1)
                    ids = struct.unpack('b', data)
                    fs.del_figure(ids)
                    print("id%(id)s" % {"id": ids})

                if com == b'M':
                    data = conn.recv(3)
                    ids, x, y = struct.unpack('bbb', data)
                    print("id%(id)s, x:%(x)s, y:%(y)s" % {"id": ids, "x": x, "y": y})

                if com == b'R':
                    data = conn.recv(1)
                    ids = struct.unpack('b', data)
                    print("id%(id)s" % {"id": ids})

            except Exception as e:
                print(e)
                break


if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)




