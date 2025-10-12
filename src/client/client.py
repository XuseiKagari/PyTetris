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
        self.sock.sendall(struct.pack('cbbbbb', b'N', figure.id, figure.x, figure.y,  figure.color.value[0],  figure.figure_number_type))

    def del_figure(self):
        figure = self.__fs.get_falling()
        self.sock.sendall(struct.pack('cb', b'D', figure.id))

    def move_figure(self):
        figure = self.__fs.get_falling()
        self.sock.sendall(struct.pack('cbbb', b'M', figure.id, figure.x, figure.y))

    def rotate_figure(self):
        figure = self.__fs.get_falling()
        self.sock.sendall(struct.pack('cb', b'R', figure.id))

    # N- новая фигура id x y color type
    # D- удалить фигуру id
    # M- переместить фигуру id x y
    # R- повернуть фигуру id

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





