import socket


def client_program():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = input(" -> ")
    while message.lower() != 'exit':

        client_socket.send(message.encode())
        message = input(" -> ")
        # return message
    # message = message.replace('Client', 'Server')

    # client_socket.send(message.encode())
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
