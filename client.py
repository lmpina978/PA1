import socket
import os

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 1234
BUFFER_SIZE = 1024

def connect_to_server():
    # Create a TCP socket for the control channel
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.connect((SERVER_ADDRESS, SERVER_PORT))
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
        #reponse = receive_message(control_socket)
        with open(file_name, 'wb') as file:
            bytes_received = 0
            while bytes_received < file_size:
                data = control_socket.recv(BUFFER_SIZE)
                file.write(data)
                bytes_received += len(data)
        print(f'{file_name} received successfully.')

        # if response == 'SUCCESS File sent.':
        #     with open(file_name, 'wb') as file:
        #         bytes_received = 0
        #         while bytes_received < file_size:
        #             print("stuck")
        #             data = control_socket.recv(BUFFER_SIZE)
        #             print("stuck 2")
        #             file.write(data)
        #             print("stuck 3")
        #             bytes_received += len(data)
        #             print("stuck 4")
        #     print(f'{file_name} received successfully.')
        # else:
        #     print(response + " LOL")
    else:
        print(response)

def put_file(control_socket, file_name):
    if os.path.isfile(file_name):
        file_size = os.path.getsize(file_name)
        send_message(control_socket, f'PUT {file_name}')
        response = receive_message(control_socket)
        if response.startswith('READY'):
            send_message(control_socket, str(file_size))
            #Maybe if here for START
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

    # print("send file good")

    # if os.path.isfile(os.path.join('files', file_name)):
    #     print("beginning verified file name is here in files")
    #     send_message(control_socket, f'FILE {file_name} {os.path.getsize(os.path.join("files", file_name))}')
    #     response = receive_message(control_socket)
    #     print("verified file name is here in files")
    #     if response == 'START':
    #         print("It good")
    #         with open(os.path.join('files', file_name), 'rb') as file:
    #             while True:
    #                 data = file.read(BUFFER_SIZE)
    #                 if not data:
    #                     break
    #                 control_socket.send(data)
    #         send_message(control_socket, 'SUCCESS File sent.')
    #     else:
    #         send_message(control_socket, 'FAILURE Failed to start file transfer.')
    # else:
    #     send_message(control_socket, 'FAILURE File not found.')

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
    control_socket = connect_to_server()
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