import socket
import os
import sys

BUFFER_SIZE = 1024

def connect_to_server(server_address, server_port):
    """Establish a TCP connection to the server"""
    try:
        control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as error:
        print('Socket creation failed with error %s' %(error))
    
    try:
        server_address = socket.gethostbyname(server_address) 
    except socket.gaierror: 
        print ('There was an error resolving the host.')
        sys.exit(1) 

    control_socket.connect((server_address, server_port))
    return control_socket

def send_message(any_socket, message):
    """Send a message to the server"""
    any_socket.send(message.encode())

def receive_message(any_socket):
    """Receive a message from the server"""
    return any_socket.recv(BUFFER_SIZE).decode()

def get_file(control_socket, file_name, server_address):
    """Request and receive a file from the server"""
    send_message(control_socket, f'GET {file_name}')
    response = receive_message(control_socket)

    if response.startswith('PORT'):
        port_number = response.split()[1]
        print(port_number)
        ephPort = int(port_number)
        print(f'Attempt to connect to port {ephPort}')
        ephSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ephSocket.connect((server_address, ephPort))
        response = receive_message(ephSocket)
        
        if response.startswith('FILE'):
            file_info = response.split()[1:]
            file_size = int(file_info[1])
            print(f'Connected, downloading {file_name} ({file_size} bytes)...')
            send_message(ephSocket, 'START')
            
            with open(file_name, 'wb') as file:
                bytes_received = 0
                
                while bytes_received < file_size:
                    data = ephSocket.recv(BUFFER_SIZE)
                    file.write(data)
                    bytes_received += len(data)
            
            print(f'{file_name} downloaded successfully.')

        ephSocket.close()
    else:
        print(response)

def put_file(control_socket, file_name, server_address):
    """Send a file to the server."""
    if os.path.isfile(file_name):
        file_size = os.path.getsize(file_name)
        send_message(control_socket, f'PUT {file_name}')
        response = receive_message(control_socket)

        if response.startswith('PORT'):
            port_number = response.split()[1]
            print(port_number)
            ephPort = int(port_number)
            print(f'Attempt to connect to port {ephPort}')
            ephSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ephSocket.connect((server_address, ephPort))
            print(f'Connected, uploading {file_name} ({int(file_size)} bytes)...')
            response = receive_message(ephSocket)
            
            if response.startswith('READY'):
                send_message(ephSocket, str(file_size))

                with open(file_name, 'rb') as file:
                    while True:
                        data = file.read(BUFFER_SIZE)
                    
                        if not data:
                            break
                    
                        ephSocket.send(data)
            
                print(f'{file_name} uploaded successfully.')
            else:
                print(response)
        
            ephSocket.close()
    else:
        print(f'Error: {file_name} not found.')

def list_files(control_socket, server_address):
    """Request a list of files from the server"""
    send_message(control_socket, 'LS')
    response = receive_message(control_socket)

    if response.startswith('PORT'):
        port_number = response.split()[1]
        print(f'Port {port_number}')
        ephPort = int(port_number)
        print(f'Attempt to connect to port {ephPort}')
        ephSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ephSocket.connect((server_address, ephPort))
        print(f'Connected, listing out the files in the server...')
        
        response = receive_message(ephSocket)
        print(response)

        ephSocket.close()

def quit(control_socket):
    """Quit the session and close the connection"""
    send_message(control_socket, 'QUIT')
    print(receive_message(control_socket))
    control_socket.close()

def main():
    if len(sys.argv) != 3:
        print('Usage: python3 client.py <server_address> <server_port>')
        sys.exit(1)
    
    server_address = sys.argv[1]

    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print('Error: Server port must be an integer.')
        sys.exit(1)
   
    print(f'Connecting with server on port {server_port}...')
    control_socket = connect_to_server(server_address, server_port)
    send_message(control_socket, 'CONNECT')

    if(receive_message(control_socket) == 'READY'):
        print('Server is ready')

        while True:
            command = input('ftp> ').strip().split()
            print(len(command))
            
            if not command:
                continue
            elif command[0].lower() == 'put':
                if(len(command) == 2):
                    file_name = command[1]
                    put_file(control_socket, file_name, server_address)
                else:
                    print('ERROR: Please write the command in the format of "put <fileName>".')
            elif command[0].lower() == 'get':
                if(len(command) == 2):
                    file_name = command[1]
                    get_file(control_socket, file_name, server_address)
                else:
                    print('ERROR: Please write the command in the format of "get <fileName>".')
            elif command[0].lower() == 'ls':
                if(len(command) == 1):
                    list_files(control_socket, server_address)
                else:
                    print("Error")
            elif command[0].lower() == 'quit':
                if(len(command) == 1):
                    quit(control_socket)
                    break
                else:
                    print("error")
            else:
                print('ERROR: Invalid command. Valid commands are "ls, get, put, quit".')
    else:
        print(f'Failed to connect with server on port {server_port}')

if __name__ == '__main__':
    main()