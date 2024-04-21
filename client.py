import socket 

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Close socket
clientSocket.close()
