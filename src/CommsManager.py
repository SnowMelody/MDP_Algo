from bluetooth import *
import serial


class BLTManager:

    def __init__(self):
        self.port = 0

    def connect_socket(self):  # initiates connection to Bluetooth and returns sockets.
        server_sock = BluetoothSocket(RFCOMM)
        server_sock.setblocking(False)
        server_sock.bind(("", self.port))
        server_sock.listen(1)
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)
        client_sock.setblocking(False)
        return server_sock, client_sock


class SerialComManager:
    def __init__(self):
        self.port = 'COM3'
        self.baud = '9600'

    def connect_serial(self):
        s = serial.Serial(self.port, self.baud)
        return s
