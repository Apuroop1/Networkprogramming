import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((IP, PORT))

s.listen()

sockets_list = [s]

clients = {}

print(f'Listening for connections on {IP}:{PORT}...')


def receive_message(c):
    try:

        message_header = c.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': c.recv(message_length)}

    except:

        return False


while True:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for new in read_sockets:

        if new == s:

            c, client_address = s.accept()

            user = receive_message(c)

            if user is False:
                continue

            sockets_list.append(c)

            clients[c] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                            user['data'].decode('utf-8')))


        else:

            message = receive_message(new)

            if message is False:
                print('Closed connection from: {}'.format(clients[new]['data'].decode('utf-8')))

                sockets_list.remove(new)

                # Remove from our list of users
                del clients[new]

                continue

            user = clients[new]
            if message["data"].decode("utf-8").lower() == 'weather':
                print("Next consecutive three days temperature in kansas city : 45c/47/34c")
            else:

                print(f'Client {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for c in clients:

                if c != new:
                    c.send(user['header'] + user['data'] + message['header'] + message['data'])

    for new in exception_sockets:
        sockets_list.remove(new)

        del clients[new]
