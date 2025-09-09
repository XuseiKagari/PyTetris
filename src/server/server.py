import socket
import struct
from threading import Thread

HOST, PORT = 'localhost', 8080
MAX_PLAYERS = 2

class Server:
    def __init__(self, addr, max_coon):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(addr)
        self.max_players = max_coon
        self.players = []

        self.s.listen(self.max_players)
        self.listen()

    def listen(self):
        while True:
            if len(self.players) < self.max_players:
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

                data = struct.unpack('c', data)



            except Exception as e:
                print(e)
                break

        self.players.remove(self.player)


if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)




