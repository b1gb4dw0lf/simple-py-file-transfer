import socket
from Client.ClientBase import ClientBase
from pickle import dumps, loads


class Client(ClientBase):

    def __init__(self, host, port, user):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super(Client, self).__init__(self.socket)

        self.target = (host, port)
        self.user = user
        self.connect()

    def connect(self):
        self.socket.connect(self.target)

    @property
    def file_list(self):
        request = {
            'command': self.COMMANDS['LIST_FILES'],
            'user': self.user
        }

        request = dumps(request)
        self.socket.send(request)
        response = loads(self.socket.recv(1024))
        return response['files']

    def receive_file(self, path, file_name):
        request = {
            'command': self.COMMANDS['DOWNLOAD_FILE'],
            'user': self.user,
            'file_name': file_name
        }

        print(request)
        request = dumps(request)
        self.socket.send(request)
        super(Client, self).receive_file(path, file_name)

    def send_file(self, path, file_name):
        request = {
            'command': self.COMMANDS['UPLOAD_FILE'],
            'user': self.user,
            'file_name': file_name
        }

        print(request)
        request = dumps(request)
        self.socket.send(request)
        super(Client, self).send_file(path, file_name)
