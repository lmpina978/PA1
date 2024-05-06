import socket
import os
import sys

BUFFER_SIZE = 1024

def start_server(server_port):
    # Create a TCP socket for the control channel
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print(f'Server listening on port {server_port}...')

    while True:
        control_socket, client_address = server_socket.accept()
        print(f'Connection established with {client_address}')
        handle_client(control_socket, client_address)
        control_socket.close()

def send_message(control_socket, message):
    control_socket.send(message.encode())

def receive_message(control_socket):
    return control_socket.recv(BUFFER_SIZE).decode()

def handle_client(control_socket, client_address):
    while True:
        command = receive_message(control_socket)

        if command.lower() == 'quit':
            send_message(control_socket, 'Goodbye.')
            print(f'Client {client_address} is leaving')
            break
        elif command.lower().startswith('get'):
            _, file_name = command.split(maxsplit=1)
            send_file(control_socket, file_name)
        elif command.lower().startswith('put'):
            _, file_name = command.split(maxsplit=1)
            receive_file(control_socket, file_name)
        else:
            list_files(control_socket)

def send_file(control_socket, file_name):
    print("send file good")

    if os.path.isfile(os.path.join('files', file_name)):
        print("beginning verified file name is here in files")
        send_message(control_socket, f'FILE {file_name} {os.path.getsize(os.path.join("files", file_name))}')
        response = receive_message(control_socket)
        print("verified file name is here in files")

        if response == 'START':
            print("It good")

            with open(os.path.join('files', file_name), 'rb') as file:
                while True:
                    data = file.read(BUFFER_SIZE)

                    if not data:
                        break
                    
                    control_socket.send(data) ##Issue here again

            #send_message(control_socket, 'SUCCESS File sent.')
        else:
            send_message(control_socket, 'FAILURE Failed to start file transfer.')
    else:
        send_message(control_socket, 'FAILURE File not found.')

def receive_file(control_socket, file_name):
    send_message(control_socket, 'READY')
    file_size = int(receive_message(control_socket))
    bytes_received = 0
    #send_message(control_socket, 'START ')

    with open(os.path.join('files', file_name), 'wb') as file:
        while bytes_received < file_size:
            data = control_socket.recv(BUFFER_SIZE)
            file.write(data)
            bytes_received += len(data)

    #send_message(control_socket, 'SUCCESS File received.')

def list_files(control_socket):
    file_list = ' '.join(os.listdir(os.path.join(os.getcwd(), 'files')))
    print(file_list)
    send_message(control_socket, file_list)

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 server.py <port>')
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print('Error: Port must be an integer.')
        sys.exit(1)

    start_server(port)

if __name__ == '__main__':
    main()

# Old code:
# import socket

# # Find port to listen to 


# # Create socket
# serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
