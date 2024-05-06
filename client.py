import socket
import os
import sys

BUFFER_SIZE = 1024

def connect_to_server(server_address, server_port):
    # Create a TCP socket for the control channel
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.connect((server_address, server_port))
    return control_socket

def send_message(control_socket, message):
    control_socket.send(message.encode())

def receive_message(control_socket):
    return control_socket.recv(BUFFER_SIZE).decode()

def get_file(control_socket, file_name):
    send_message(control_socket, f'GET {file_name}')
    response = receive_message(control_socket)

    if response.startswith('FILE'):
        file_info = response.split()[1:]
        file_size = int(file_info[1])
        print(f'Receiving {file_name} ({file_size} bytes)...')
        send_message(control_socket, 'START')

        with open(file_name, 'wb') as file:
            bytes_received = 0

            while bytes_received < file_size:
                data = control_socket.recv(BUFFER_SIZE)
                file.write(data)
                bytes_received += len(data)
        
        print(f'{file_name} received successfully.')
    else:
        print(response)

def put_file(control_socket, file_name):
    if os.path.isfile(file_name):
        file_size = os.path.getsize(file_name)
        send_message(control_socket, f'PUT {file_name}')
        response = receive_message(control_socket)

        if response.startswith('READY'):
            send_message(control_socket, str(file_size))

            with open(file_name, 'rb') as file:
                while True:
                    data = file.read(BUFFER_SIZE)
                    
                    if not data:
                        break
                    
                    control_socket.send(data)
            
            print(f'{file_name} uploaded successfully.')
        else:
            print(response)
    else:
        print(f'Error: {file_name} not found.')

def list_files(control_socket):
    send_message(control_socket, 'LS')
    response = receive_message(control_socket)
    print(response)

def quit(control_socket):
    send_message(control_socket, 'QUIT')
    response = receive_message(control_socket)
    print(response)
    control_socket.close()

def main():
    if len(sys.argv) != 3:
        print('Usage: python3 client.py <host_address> <host_port>')
        sys.exit(1)

    host_address = sys.argv[1]
    
    try:
        host_port = int(sys.argv[2])
    except ValueError:
        print('Error: Server port must be an integer.')
        sys.exit(1)
   
    control_socket = connect_to_server(host_address, host_port)
    
    while True:
        command = input('ftp> ').strip().split()
        valid_command = len(command) == 2
        print(len(command))

        if not command:
            continue
        elif command[0].lower() == 'put':
            if(valid_command):
                file_name = command[1]
                put_file(control_socket, file_name)
            else:
                print('ERROR: Please write the command in the format of "put <fileName>".')
        elif command[0].lower() == 'get':
            if(valid_command):
                file_name = command[1]
                get_file(control_socket, file_name)
            else:
                print('ERROR: Please write the command in the format of "get <fileName>".')
        elif command[0].lower() == 'ls':
            if(valid_command):
                list_files(control_socket)
            else:
                print("Error")
        elif command[0].lower() == 'quit':
            if(valid_command):
                quit(control_socket)
                break
            else:
                print("error")
        else:
            print('ERROR: Invalid command. Valid commands are "ls, get, put, quit".')

if __name__ == '__main__':
    main()

# Old Code:
# import socket
# import sys
# import os

# # Create client socket
# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Specify max amount of bytes to be sent in each packet
# max = 1024

# # Will count the amount of packets that were sent from client to server
# packetCount = 0

# # Open file for string
# txtfile = open("untitled.txt", "r")
# filename = sys.argv[1]

# print("Opening " + filename)

# txtdata = txtfile.read()

# # Check if data is string and get size in bytes
# stringcheck = isinstance(txtdata, str)
# stringsize = os.path.getsize("untitled.txt")



# print("A total of " + packetCount + " packets and " + "0 bytes have been sent.")
# # Close socket
# clientSocket.close()