import socket
from Server.ClientHandler import ClientHandler
from os import walk


class Server:

    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1', port))

    def start(self):
        self.socket.listen(5)
        print('Listening and accepting connections.')

        connection = None
        while True:
            try:
                connection, addr = self.socket.accept()
                print('Received connection from {}'.format(addr))
                client_thread = ClientHandler(connection)
                client_thread.start()
            except KeyboardInterrupt:
                connection.close()
                self.socket.close()
                break
