import socket
import struct
from threading import Thread
from figure_s import FigureServer
from figure_storage_s import FigureStorageServer

HOST, PORT = 'localhost', 65432
MAX_PLAYERS = 2
FULL_FIGURE_DESC = 'bbbbb'
FIGURE_ROTATE = 'b'
FIGURE_MOVE = 'bbb'
FIGURE_DEL = 'b'

def recv_all(conn, length: int) -> bytes:
    data = b''
    while len(data) < length:
        packet = conn.recv(length - len(data))
        if not packet:
            return None
        data += packet
    return data


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
        fs = FigureStorageServer()
        while True:
            try:
                com = recv_all(conn, 1)

                if not com:
                    break
                com = struct.unpack('c', com)[0]

                if com == b'N':
                    data = recv_all(conn, 5)
                    ids, x, y, color, fig_type = struct.unpack(FULL_FIGURE_DESC, data)
                    fig = FigureServer(ids, x, y, color, fig_type)
                    fs.set_falling(fig)
                    print(f"{ids=}, {x=}, {y}, {color=}, {fig_type=}")

                if com == b'D':
                    data = recv_all(conn, 1)
                    ids = struct.unpack(FIGURE_DEL, data)
                    fs.del_figure(ids)
                    print(f"{ids=}")

                if com == b'M':
                    data = recv_all(conn, 3)
                    ids, x, y = struct.unpack(FIGURE_MOVE, data)
                    print(f"{ids=}, {x=}, {y=}")

                if com == b'R':
                    data = recv_all(conn, 1)
                    ids = struct.unpack(FIGURE_ROTATE, data)
                    print(f"{ids=}")

            except Exception as e:
                print(e)
                break


if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)




