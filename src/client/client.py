import socket
import struct
from threading import Thread


class Client:
    def __init__(self, addr, figure_storage):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)
        self.__fs = figure_storage
        Thread(target=self.get_new_figure,args=()).start()

    def send_new_figure(self):
        figure = self.__fs.get_falling()
        self.sock.sendall(struct.pack('bbbb', figure.x, figure.y,  figure.color.value[0],  figure.figure_number_type))

    def get_new_figure(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    print("Сервер закрыл соединение.")
                    break

                x, y, color, figure_type = struct.unpack('bbbb', data)
                print("x:%(x)s, y:%(y)s, color:%(color)s, type:%(type)s" % {"x": x, "y": y, "color": color, "type": figure_type})
            except ConnectionResetError:
                print("Соединение было сброшено сервером.")
                break
            except Exception as e:
                print(f"Ошибка при приеме данных: {e}")
                break





