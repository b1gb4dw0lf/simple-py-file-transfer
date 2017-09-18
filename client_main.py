from Client.Client import Client


if __name__ == "__main__":

    client = Client('127.0.0.1', 4567, {'username': 'kaan'})
    file = client.file_list[0]
    print(file)
    client.send_file('./users/recv', '9781784391362-UNITY_5X_COOKBOOK.pdf')
    client.socket.close()
