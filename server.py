import socket
import os
import sys

BUFFER_SIZE = 1024

def start_server(server_port):
  """Main function to start the server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print(f'Server listening on port {server_port}...')

    while True:
        control_socket, client_address = server_socket.accept()

        if(receive_message(control_socket) == 'CONNECT'):
            print(f'Connection established with {client_address}')
            send_message(control_socket, 'READY')
            handle_client(control_socket, client_address)
            control_socket.close()
        else:
            print(f'Failed to connect with {client_address}')
            send_message(control_socket, 'FAILURE')

def send_message(any_socket, message):
  """Sends message through given socket"""
    any_socket.send(message.encode())

def receive_message(any_socket):
  """Receives message from given socket"""
    return any_socket.recv(BUFFER_SIZE).decode()

def handle_client(control_socket, client_address):
  """Handle client requests"""
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
  """Send a file to the client"""
    print("In send_file function")

    if os.path.isfile(os.path.join('files', file_name)):
        # Establish a new data channel
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind(('', 0))  # Bind to an ephemeral port
        data_socket.listen(1)

        data_port = data_socket.getsockname()[1]
        send_message(control_socket, f'PORT {data_port}')

        data_connection, data_address = data_socket.accept()
        print(f'Data connection established with {data_address} for {file_name}')

        send_message(data_connection, f'FILE {file_name} {os.path.getsize(os.path.join("files", file_name))}')
        response = receive_message(data_connection)
        print("Data_socket good in send_file")

        if response == 'START':
            print("It good")

            with open(os.path.join('files', file_name), 'rb') as file:
                while True:
                    data = file.read(BUFFER_SIZE)

                    if not data:
                        break
                    
                    data_connection.send(data)

            #send_message(data_connection, 'SUCCESS File sent.')
        else:
            send_message(data_connection, 'FAILURE Failed to start file transfer.')
        
        data_connection.close()
        data_socket.close()
    else:
        send_message(control_socket, 'FAILURE File not found.')

def receive_file(control_socket, file_name):
  """Receive a file from the client"""
    # Establish a new data channel
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('', 0))  # Bind to an ephemeral port
    data_socket.listen(1)

    data_port = data_socket.getsockname()[1]
    send_message(control_socket, f'PORT {data_port}')

    data_connection, data_address = data_socket.accept()
    print(f'Data connection established with {data_address} for {file_name}')

    send_message(data_connection, 'READY')
    file_size = int(receive_message(data_connection))
    bytes_received = 0
    #send_message(control_socket, 'START ')

    with open(os.path.join('files', file_name), 'wb') as file:
        while bytes_received < file_size:
            data = data_connection.recv(BUFFER_SIZE)
            file.write(data)
            bytes_received += len(data)
    
    data_connection.close()
    data_socket.close()
    #send_message(control_socket, 'SUCCESS File received.')

def list_files(control_socket):
  """Send a list of files to the client"""
    # Establish a new data channel
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('', 0))  # Bind to an ephemeral port
    data_socket.listen(1)

    data_port = data_socket.getsockname()[1]
    send_message(control_socket, f'PORT {data_port}')

    data_connection, data_address = data_socket.accept()
    print(f'Data connection established with {data_address}')

    file_list = ' '.join(os.listdir(os.path.join(os.getcwd(), 'files')))
    print(file_list)
    send_message(data_connection, file_list)

    data_connection.close()
    data_socket.close()

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