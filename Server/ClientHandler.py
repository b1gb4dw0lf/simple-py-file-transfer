from Client.ClientBase import ClientBase
from pickle import dumps, loads
from os import walk, mkdir
from threading import Thread


class ClientHandler(Thread, ClientBase):

    def __init__(self, socket):
        Thread.__init__(self)
        ClientBase.__init__(self, socket)

    def run(self):
        print('Client Thread is active.')
        while True:
            try:
                request = loads(self.socket.recv(1024))
                print(request)
                command = request['command']
                path = './users/{}/'.format(request['user']['username'])

                if command == self.COMMANDS['LIST_FILES']:
                    self.list_user_directory(path)
                elif command == self.COMMANDS['UPLOAD_FILE']:
                    file_name = request['file_name']
                    self.receive_file(path, file_name)
                elif command == self.COMMANDS['DOWNLOAD_FILE']:
                    file_name = request['file_name']
                    self.send_file(path, file_name)
            except EOFError:
                pass

    def list_user_directory(self, path):
        try:
            file_names = next(walk(path))[2]
            reply = {'files': file_names}
            reply = dumps(reply)
            self.socket.send(reply)
        except StopIteration:
            mkdir(path)
            self.list_user_directory(path)
