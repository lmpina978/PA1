import socket
import os

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 1234
BUFFER_SIZE = 1024

def connect_to_server():
    """Establish a TCP connection to the server"""
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    return control_socket

def send_message(control_socket, message):
    """Send a message to the server"""
    control_socket.send(message.encode())

def receive_message(control_socket):
    """Receive a message from the server"""
    return control_socket.recv(BUFFER_SIZE).decode()

def get_file(control_socket, file_name):
    """Request and receive a file from the server"""
    send_message(control_socket, f'GET {file_name}')
    response = receive_message(control_socket)
    if response.startswith('FILE'):
        _, _, file_size = response.split()
        file_size = int(file_size)
        print(f'Receiving {file_name} ({file_size} bytes)...')
        send_message(control_socket, 'START')
        with open(file_name, 'wb') as file:
            bytes_received = 0
            while bytes_received < file_size:
                data = control_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)
                bytes_received += len(data)
        print(f'{file_name} received successfully')
    else:
        print(response)

def put_file(control_socket, file_name):
    """Send a file to the server."""
    if os.path.isfile(file_name):
        file_size = os.path.getsize(file_name)
        send_message(control_socket, f'PUT {file_name} {file_size}')
        if receive_message(control_socket) == 'READY':
            with open(file_name, 'rb') as file:
                send_data_from_file(file, control_socket)
            print(f'{file_name} uploaded successfully')
        else:
            print('Server was not ready to receive the file')
    else:
        print(f'Error: File {file_name} not found')

def send_data_from_file(file, control_socket):
    """Sends data from a file to the server"""
    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            break
        control_socket.send(data)

def list_files(control_socket):
    """Request a list of files from the server"""
    send_message(control_socket, 'LS')
    print(receive_message(control_socket))

def quit(control_socket):
    """Quit the session and close the connection"""
    send_message(control_socket, 'QUIT')
    print(receive_message(control_socket))
    control_socket.close()

def main():
    control_socket = connect_to_server()
    try:
        while True:
            command = input('ftp> ').strip()
            if command.lower() == 'quit':
                quit(control_socket)
                break
            elif command.lower().startswith('get'):
                _, file_name = command.split(maxsplit=1)
                get_file(control_socket, file_name)
            elif command.lower().startswith('put'):
                _, file_name = command.split(maxsplit=1)
                put_file(control_socket, file_name)
            elif command.lower() == 'ls':
                list_files(control_socket)
            else:
                print('Invalid command.')
    except Exception as e:
        print(f"An error occurred: {e}")
        control_socket.close()

if __name__ == '__main__':
    main()