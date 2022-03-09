import socket
import itertools


# When the socket object is created, it will establish connection automatically
class socket_creation:
    def __init__(self, ip_address, port):
        self.address = (ip_address, port)
        self.client_socket = socket.socket()

        self.client_socket.connect(self.address)

    def receive_response(self):
        response = self.client_socket.recv(1024)
        return response.decode()

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def end_connection(self):
        self.client_socket.close()


# digits_ascii is needed to determine with what alphanumeric characters the password will be made of
class finder:
    def __init__(self):
        self.file = open('logins.txt', 'r')

    def username_generator(self):
        password = self.file.readlines(1)[0].strip('\n')
        username_creator = map(lambda x: ''.join(x),
                               itertools.product(*([letter.lower(), letter.upper()] for letter in password)))
        username_creator = set(list(username_creator))
        return username_creator
