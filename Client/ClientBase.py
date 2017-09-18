import socket as SOCKET
from sys import getsizeof
from os.path import getsize


class ClientBase:
    COMMANDS = {
        'LIST_FILES': 'LIST_FILES',
        'UPLOAD_FILE': 'UPLOAD_FILE',
        'DOWNLOAD_FILE': 'DOWNLOAD_FILE'
    }

    def __init__(self, socket):
        self.socket = socket

    def receive_file(self, path, file_name):
        with open('{}/{}'.format(path, file_name), 'w'):
            pass
        with open('{}/{}'.format(path, file_name), 'ab') as file:
            while True:
                data = self.socket.recv(1024)
                print("Received {} bytes".format(file.tell()))
                if not data:
                    break

                file.write(data)
                self.socket.send('OK'.encode())

    def send_file(self, path, file_name):
        file_size = getsize('{}/{}'.format(path, file_name))
        with open('{}/{}'.format(path, file_name), 'rb') as file:
            file_bytes = file.read(1024)
            while file_bytes:
                if not file_bytes:
                    break
                print("Bytes sending, {} bytes remaining".format(file_size - file.tell()))
                self.socket.send(file_bytes)
                self.socket.recv(1024)
                file_bytes = file.read(1024)
            self.socket.shutdown(SOCKET.SHUT_WR)
