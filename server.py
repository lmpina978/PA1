import socket
import os

SERVER_PORT = 1234
BUFFER_SIZE = 1024
FILES_DIR = 'files'

def start_server():
    """Main function to start the server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', SERVER_PORT))
    server_socket.listen(1)
    print(f'Server listening on port {SERVER_PORT}...')

    try:
        while True:
            control_socket, client_address = server_socket.accept()
            print(f'Connection established with {client_address}')
            handle_client(control_socket)
            control_socket.close()
    finally:
        server_socket.close()

def handle_client(control_socket):
    """Handle client requests"""
    while True:
        command = receive_message(control_socket)
        if not command:
            break

        process_command(control_socket, command)

def process_command(control_socket, command):
    """Process each command sent by the client"""
    command = command.lower()
    if command == 'quit':
        send_message(control_socket, 'Goodbye.')
        return
    if command.startswith('get'):
        _, file_name = command.split(maxsplit=1)
        send_file(control_socket, file_name)
    elif command.startswith('put'):
        _, file_name = command.split(maxsplit=1)
        receive_file(control_socket, file_name)
    elif command == 'ls':
        list_files(control_socket)
    else:
        send_message(control_socket, f'Invalid command {command}')

def send_message(control_socket, message):
    """Sends message through given socket"""
    control_socket.send(message.encode())

def receive_message(control_socket):
    """Receives message from given socket"""
    return control_socket.recv(BUFFER_SIZE).decode()

def send_file(control_socket, file_name):
    """Send a file to the client"""
    file_path = os.path.join(FILES_DIR, file_name)
    if os.path.isfile(file_path):
        file_size = os.path.getsize(file_path)
        send_message(control_socket, f'FILE {file_name} {file_size}')
        if receive_message(control_socket) == 'START':
            with open(file_path, 'rb') as file:
                send_data_from_file(file, control_socket)
            send_message(control_socket, 'SUCCESS File sent')
        else:
            send_message(control_socket, 'FAILURE Failed to start file transfer')
    else:
        send_message(control_socket, 'FAILURE File not found')

def receive_file(control_socket, file_name):
    """Receive a file from the client"""
    send_message(control_socket, 'READY')
    file_size = int(receive_message(control_socket))
    send_message(control_socket, 'START ')
    with open(os.path.join(FILES_DIR, file_name), 'wb') as file:
        receive_data_to_file(file, file_size, control_socket)
    send_message(control_socket, 'SUCCESS File received')

# Helper functions

def send_data_from_file(file, control_socket):
    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            break
        control_socket.send(data)

def receive_data_to_file(file, file_size, control_socket):
    bytes_received = 0
    while bytes_received < file_size:
        data = control_socket.recv(BUFFER_SIZE)
        file.write(data)
        bytes_received += len(data)

def list_files(control_socket):
    """List files in the directory"""
    files = ' '.join(os.listdir(FILES_DIR))
    send_message(control_socket, files)

if __name__ == '__main__':
    start_server()